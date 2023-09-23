from .models import *

from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import *
from django.core.exceptions import ObjectDoesNotExist
from core import models as coremodels
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination

class categoryViewAPI(ListCreateAPIView):

    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes = [permissions.IsAuthenticated, ]

class categoryUpdateViewAPI(RetrieveUpdateAPIView):

    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def retrieve(self,request,*args,**kwargs):
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error":"Does not exist"},status=400)
        
        serializer = self.get_serializer(instance)

        return Response(serializer.data,status=200)

    def partial_update(self,request,*args,**kwargs):
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error":"Does not exist"},status=400)
        
        serializer = self.get_serializer(instance,data=request.data,partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=200)

class subcategoryAPI(ListCreateAPIView):
    queryset=Subcategory.objects.all()
    serializer_class=SubcategorySerializer
    permission_classes = [permissions.IsAuthenticated, ]

class SubcategoryUpdateViewAPI(RetrieveUpdateAPIView):
    queryset=Subcategory.objects.all()
    serializer_class=SubcategorySerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def retrieve(self,request,*args,**kwargs):
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error":"Does not exist"},status=400)
        
        serializer = self.get_serializer(instance)

        return Response(serializer.data,status=200)

    def partial_update(self,request,*args,**kwargs):
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error":"Does not exist"},status=400)
        
        serializer = self.get_serializer(instance,data=request.data,partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=200)

class subcategoryslugapi(ListAPIView):

    queryset=Subcategory.objects.all()
    serializer_class=SubcategorySerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self,request,*args,**kwargs):

        queryset = self.queryset.filter(category__slug=kwargs["name"])

        serializer = self.get_serializer(queryset,many=True)

        return Response(serializer.data,status=200)
    
class ProductAddAPI(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self,request,*args,**kwargs):

        if not request.user.is_designer:
            return Response({"error":"User is not an designer"},status=401)
        
        designer = coremodels.Designer.objects.get(user=request.user)

        request.data["designer"]=designer

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = self.queryset.get(id=serializer.data["id"])

        followers = coremodels.Followers.objects.get(designer=designer)

        for i in followers.followers_id.all():

            home = MerchantHomeProduct.objects.get(id=i)

            home.product.add(instance)

            home.save()
        
        return Response(serializer.data,status=200)
    
class DesignerProductList(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 30

    def list(self,request,*args,**kwargs):

        if not request.user.is_designer:
            return Response({"error":"User is not an designer"},status=401)
        
        designer = coremodels.Designer.objects.get(user=request.user)

        queryset = self.queryset.filter(designer=designer)

        serializer = self.get_serializer(queryset,many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)

class DesignerProductEditApi(RetrieveUpdateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self,request,*args,**kwargs):

        if not request.user.is_designer:
            return Response({"error":"User is not an designer"},status=401)
        
        designer = coremodels.Designer.objects.get(user=request.user)

        try:
            queryset = self.queryset.get(designer=designer,id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error":"Product doesnot belong to designer or product doesnt exist"})

        serializer = self.get_serializer(queryset)

        return Response(serializer.data,status=200)
    
    def partial_update(self,request,*args,**kwargs):

        if not request.user.is_designer:
            return Response({"error":"User is not an designer"},status=401)
        
        designer = coremodels.Designer.objects.get(user=request.user)

        try:
            queryset = self.queryset.get(designer=designer,id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error":"Product doesnot belong to designer or product doesnt exist"})

        serializer = self.get_serializer(queryset,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=200)


class ProductListApi(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductDisplaySerializer
    permission_classes = [permissions.IsAuthenticated, ]
    filter_backends = [SearchFilter,DjangoFilterBackend]
    search_fields = ['code', 'machine','name']
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    pagination_class.page_size = 30

    def get_queryset(self):

        queryset = self.queryset.filter(sub_category__slug=self.kwargs["sub"],is_active=True)

        return queryset

class AllProductsAPI(ListAPIView):

    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDisplaySerializer
    permission_classes = [permissions.IsAuthenticated, ]
    filter_backends = [SearchFilter,DjangoFilterBackend]
    search_fields = ['code', 'machine','name']
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    pagination_class.page_size = 30

class DesignerHomeProduct(RetrieveAPIView):

    queryset = MerchantHomeProduct.objects.all()
    serializer_class = MechantHomeSerializer
    permission_classes = [permissions.IsAuthenticated, ]


# class AllProductView(APIView):
#     serializer_class=ProductSerializer
#     queryset=Product.objects.all()
#     permission_classes = [permissions.IsAuthenticated, ]

#     def get(self, request, format=None):
#         try:
#             pro = Product.objects.all()
#             serializer = ProductSerializer(pro, many=True)
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         except Product.DoesNotExist:
#             return status.HTTP_404_NOT_FOUND

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request):
#         q = Product.objects.get(product_id=request.data['product_id'])
#         q.delete()
#         return Response(data='Delete', status=status.HTTP_410_GONE)

#     def put(self, request):
#         q = Product.objects.get(product_id=request.data['product_id'])
#         serializer = ProductSerializer(q, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CategoryProductView(generics.ListCreateAPIView):

#     model = Product
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated, ]
#     def get_queryset(self):
#         queryset = Product.objects.all()
#         cat = self.request.query_params.get('cat')
#         subcat = self.request.query_params.get('subcat')

#         if cat and subcat:
#             queryset = queryset.filter(category=cat)
#             queryset = queryset.filter(sub_category=subcat)
#         elif cat:
#             queryset = queryset.filter(category=cat)
#         elif subcat:
#             queryset = queryset.filter(sub_category=subcat)
#         return queryset


# class FilterProductAPIView(generics.ListAPIView):

#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated, ]

#     def get_queryset(self):
#         queryset= Product.objects.all()

#         min_stitch=self.request.query_params.get('min_stitch', None)
#         if min_stitch is not None:
#             queryset=queryset.filter(stitch__gte=min_stitch)

#         max_stitch=self.request.query_params.get('max_stitch', None)
#         if max_stitch is not None:
#             queryset=queryset.filter(stitch__lte=max_stitch)

#         min_area=self.request.query_params.get('min_area', None)
#         if min_area is not None:
#             queryset=queryset.filter(area__gte=min_area)

#         max_area=self.request.query_params.get('max_area', None)
#         if max_area is not None:
#             queryset=queryset.filter(area__lte=max_area)

#         min_width=self.request.query_params.get('min_width', None)
#         if min_width is not None:
#             queryset=queryset.filter(width__gte=min_width)

#         max_width=self.request.query_params.get('max_width', None)
#         if max_width is not None:
#             queryset=queryset.filter(width__lte=max_width)

#         min_height=self.request.query_params.get('min_height', None)
#         if min_height is not None:
#             queryset=queryset.filter(height__gte=min_height)

#         max_height=self.request.query_params.get('max_height', None)
#         if max_height is not None:
#             queryset=queryset.filter(height__lte=max_height)

#         min_needle=self.request.query_params.get('min_needle', None)
#         if min_needle is not None:
#             queryset=queryset.filter(needle__gte=min_needle)

#         max_needle=self.request.query_params.get('max_needle', None)
#         if max_needle is not None:
#             queryset=queryset.filter(needle__lte=max_needle)
        
#         return queryset


# class ProductSearchAPIView(generics.ListAPIView):

#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [filters.SearchFilter]
#     permission_classes = [permissions.IsAuthenticated, ]
#     search_fields = ['category', 'sub_category','machine']


