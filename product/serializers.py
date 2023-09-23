from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

from core.serializers import DesignerMinSerializer

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model= Product
        fields = '__all__'
class ProductDisplaySerializer(serializers.ModelSerializer):
    
    designer = DesignerMinSerializer(read_only=True,many=False)
    category = CategorySerializer(read_only=True)
    sub_category = SubcategorySerializer(read_only=True)
    file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_file(self,obj):
        return None


class ProductMinDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model= Product
        fields = ["name","image1","image2","image3","image4","price"]

class MechantHomeSerializer(serializers.ModelSerializer):

    product = ProductMinDisplaySerializer(many=True)

    class Meta:
        model = MerchantHomeProduct
        fields = "__all__"

class ProductListSerializer(serializers.ModelSerializer):

    file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_file(self,obj):
        return None

class OrderedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model= Product
        fields = ["name","image1","image2","image3","image4","file"]

