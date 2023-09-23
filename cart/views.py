from .models import Product_saved, Cart,Items
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from core.models import Merchant, Designer
from product.models import Product
from .models import *
import datetime
from django.shortcuts import render, get_object_or_404

# Create your views here.
class SavedProductView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, format=None):
        if not request.user.is_merchant:
            return Response({"error":"User is not a merchant"},status=401)
        
        merchant = Merchant.objects.get(user=request.user)
        try:
            pro = Product_saved.objects.filter(u_id=merchant)
            serializer = ProductSavedSerializer(pro, many=True)
            return Response(serializer.data, status=200)
        except Product_saved.DoesNotExist:
            return Response("Not found",status=404)

    def post(self, request):
        if not request.user.is_merchant:
            return Response({"error":"User is not a merchant"},status=401)
        
        merchant = Merchant.objects.get(user=request.user)

        saved,created = Product_saved.objects.get_or_create(merchant=merchant) 
        try:
            product = Product.objects.get(product_id=request.data.get('product_id'))
            saved.product.add(product)
        except:
            return Response("Wrong Product Id", status=404)

        saved.save()
        serializer = ProductSavedSerializer(saved,many=False)

        return Response(serializer.data, status=200)

class RemoveSavedProductView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        if not request.user.is_merchant:
            return Response({"error":"User is not a merchant"},status=401)
        
        merchant = Merchant.objects.get(user=request.user)

        saved,created = Product_saved.objects.get_or_create(merchant=merchant) 
        try:
            product = Product.objects.get(product_id=request.data.get('product_id'))
            saved.product.remove(product)
        except:
            return Response("Wrong Product Id", status=404)

        saved.save()
        serializer = ProductSavedSerializer(saved,many=False)

        return Response(serializer.data, status=200)

class AddtoCartView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        if not request.user.is_merchant:
            return Response({"error":"User is not a merchant"},status=401)
        
        merchant = Merchant.objects.get(user=request.user)

        cart = Cart.objects.filter(merchant=merchant,ordered=False,singleproduct=False)

        if cart.exists():
            cart=cart[0]
        else:
            cart = Cart.objects.create(merchant=merchant,ordered=False,singleproduct=False) 
        
        try:
            product = Product.objects.get(product_id=request.data['product_id'])
            item = Items.object.create(cart=cart,product=product,quantity=request.data['quantity'])
        except:
            return Response("Wrong Product Id", status=404)

#        saved.save()

        return Response("Added", status=200)

class CartView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def retrieve(self,request,*args,**kwargs):

        if not request.user.is_merchant:
            return Response({"error":"User is not a merchant"},status=401)
        
        merchant = Merchant.objects.get(user=request.user)   

        cart = Cart.objects.filter(merchant=merchant, ordered=False, singleproduct=False)
        if cart.exists():
            cart =  cart[0]
        else:
            return Response("No Active cart",status=404)
        
        serializer = self.get_serializer(cart)

        return Response(serializer.data,status=200)

class RemovefromCartView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        if not request.user.is_merchant:
            return Response({"error":"User is not a merchant"},status=401)
        
        merchant = Merchant.objects.get(user=request.user)

        #cart = Cart.objects.filter(merchant=merchant,ordered=False,singleproduct=False)
        try:
            cart = Cart.objects.get(merchant=merchant,id=request.data["cartid"])
        except :
            return Response({"error":"cart id wrong"},status=400)
        
        try:
            item = Items.object.get(id=request.data["item"])
            item.delete()
        except:
            return Response("Wrong Item Id", status=404)

 #       saved.save()

        return Response("Removed", status=200)


# class BillView(APIView):

#     permission_classes = [permissions.IsAuthenticated, ]

#     def get(self, request, format=None):
#         try:
#             ord = Orders.objects.filter(bill_id=request.data['bill_id'])
#             serializer = BillSerializer(ord)
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         except Orders.DoesNotExist:
#             return status.HTTP_404_NOT_FOUND


class ConfirmPaymentAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args,**kwargs):

        if not request.user.is_merchant:
            return Response({"error":"User is not a merchant"},status=401)
        
        merchant = Merchant.objects.get(user=request.user)

        razorpay_payment_id=request.data.get('razorpay_payment_id',None)
        razorpay_order_id=request.data.get('razorpay_order_id',None)
        razorpay_signature=request.data.get('razorpay_signature',None)

        params_dict = {
            'razorpay_payment_id' : razorpay_payment_id,
            'razorpay_order_id' : razorpay_order_id,
            'razorpay_signature' : razorpay_signature
        }

        try:
            cart=Cart.objects.get(merchant=merchant,ordered=False,orderid=razorpay_order_id)
        except :
            return Response({"message":"No such payment data found."},status=status.HTTP_400_BAD_REQUEST)

        try:
            client.utility.verify_payment_signature(params_dict)
        except:
            if cart.single_product == True:
                cart.delete()
            raise Exception('Razorpay Signature Verification Failed')

        cart.ordered=True
        cart.paymentid=razorpay_payment_id
        cart.save()

        for i in Items.objects.filter(cart=cart):
            obj=RecentOrdersDesigner.objects.create(
            merchant=merchant,
            designer=i.product.designer,
            product=i.product,
            quantity=i.quantity,
            amount=i.product.price*i.quantity)
            obj.save()

        # new_ord = Orders.objects.create(buyer_name=request.user.username,cart_id=Cart);
        # new_ord.save()
        return Response({"message":"Payment Successful"}, status=status.HTTP_200_OK)


class PastOrderView(generics.ListAPIView):

    queryset = Cart.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self,request,*args,**kwargs):

        if not request.user.is_merchant:
            return Response({"error":"User is not a merchant"},status=401)
        
        merchant = Merchant.objects.get(user=request.user)

        queryset = self.queryset(merchant=merchant,ordered=True)

        serializer = self.get_serializer(queryset,many=True)

        return Response(serializer.data,status=200)        

class OrderedItems(generics.ListAPIView):

    queryset = Items.objects.all()
    serializer_class = ItemsOrderSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self,request,*args,**kwargs):
        if not request.user.is_merchant:
            return Response({"error":"User is not a merchant"},status=401)
        
        merchant = Merchant.objects.get(user=request.user)

        try:
            cart = Cart.objects.get(merchant=merchant,id=kwargs["id"],ordered=True)
        except:
            return Response({"error":"Invalid Cart"},status=400)

        queryset = self.queryset(cart=cart)

        serializer = self.get_serializer(queryset,many=True)

        return Response(serializer.data,status=200)
# class PastOrdersAPIView(generics.ListAPIView):

#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = [permissions.IsAuthenticated, ]

#     def get_queryset(self):
#         queryset =Cart.objects.filter(ordered=True,user=self.request.user).order_by("-id")
       
#         from_date = self.request.query_params.get('from_date', None)
#         if from_date is not None:
#             from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
#             queryset = queryset.filter(ordereddate__date__gte = from_date).order_by("-id")

#         to_date = self.request.query_params.get('to_date', None)

#         if to_date is not None:
#             to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
#             queryset = queryset.filter(ordereddate__date__lte = to_date).order_by("-id")

#         return queryset
  

# class RecentOrdersListAPIView(APIView):

#     permission_classes = [permissions.IsAuthenticated, ]

#     def get(self, request, *args,**kwargs):
        
#         designer=Designer.objects.get(user=request.user)
#         orders = RecentOrdersDesigner.objects.filter(designer=designer)

#         serializer = RecentOrdersDesignerSerializer(orders,many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)


# class TotalRevenueAPIView(APIView):

#     permission_classes = [permissions.IsAuthenticated, ]

#     def get(self, request, *args,**kwargs):
        
#         designer=Designer.objects.get(user=request.user)
#         orders = RecentOrdersDesigner.objects.filter(designer=designer)

#         total_revenue=0
#         for i in orders:
#             total_revenue+=i.amount

#         msg = {
#             "Total Revenue":total_revenue,
#         }
        
#         return Response(data=msg,status=status.HTTP_200_OK)


# class MonthlyRevenueAPIView(APIView):

#     permission_classes = [permissions.IsAuthenticated, ]

#     def get(self, request, *args,**kwargs):
        
#         designer=Designer.objects.get(user=request.user)
#         month=datetime.date.today().month
#         orders = RecentOrdersDesigner.objects.filter(designer=designer,date__month=month)

#         monthly_revenue=0
#         for i in orders:
#             monthly_revenue+=i.amount

#         msg = {
#             "Monthly Revenue":monthly_revenue,
#         }
        
#         return Response(data=msg,status=status.HTTP_200_OK)
        