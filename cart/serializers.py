from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Product_saved, Cart, Items,Orders, RecentOrdersDesigner, Merchant, Designer
from product.serializers import *
from core.serializers import *
from django.conf import settings
import razorpay

class ProductSavedSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(many=True,read_only=True)
    merchant = MerchantSerializer(many=True,read_only=True)
    class Meta:
        model = Product_saved
        fields = '__all__'

class ItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model=Items
        fields='__all__'

class ItemsCartSerializer(serializers.ModelSerializer):
    product = ProductMinDisplaySerializer(read_only=True)

    class Meta:
        model=Items
        fields='__all__'
class CartSerializer(serializers.ModelSerializer):

    order_id=serializers.SerializerMethodField(read_only=True)
    items=ItemsCartSerializer(read_only=True,many=True)

    class Meta:
        model=Cart
        fields='__all__'

    def get_order_id(self,obj):

        amount=0
        items=Items.objects.filter(cart=obj)
        print(items)

        for i in items:
            amount+=(i.product.price*i.quantity)
        
        print(amount)
        
        if amount > 0 :
            client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
            orderid=client.order.create(data={"amount":amount*100,"currency":"INR","payment_capture":"1"})
            obj.payment=amount
            obj.orderid=orderid["id"]
            
            obj.save()
        return None
    


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model=Orders
        fields='__all__'
        depth = 2


class RecentOrdersDesignerSerializer(serializers.ModelSerializer):

    class Meta:
        model=RecentOrdersDesigner
        fields='__all__'
        depth=2

class OrderSerializer(serializers.ModelSerializer):

    items=ItemsCartSerializer(read_only=True,many=True)

    class Meta:
        model=Cart
        fields='__all__'

class ItemsOrderSerializer(serializers.ModelSerializer):

    product = OrderedProductSerializer(read_only=True)

    class Meta:
        model = Items
        fields = "__all__"