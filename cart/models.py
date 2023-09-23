from django.db import models
from core.models import User,Designer,Merchant
from product.models import Product

class Product_saved(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT, null=True)
    product = models.ManyToManyField(Product)
    s_created = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    merchant=models.ForeignKey(Merchant, on_delete=models.PROTECT)
    startdate=models.DateField(auto_now_add=True)
    ordereddate=models.DateTimeField(auto_now=True)
    ordered=models.BooleanField(default=False)
    orderid=models.CharField(max_length=200,blank=True,null=True)
    payment=models.IntegerField(default=0)
    singleproduct=models.BooleanField(default=False)
    paymentid=models.CharField(max_length=200,blank=True,null=True)


    def __str__(self):
        return self.merchant.name


class Items(models.Model):
    cart=models.ForeignKey(Cart,related_name='items',on_delete=models.PROTECT)
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return self.cart.merchant.name



class Orders(models.Model):
    buyer_name = models.CharField(max_length=50, default="Unknown")
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.id


class RecentOrdersDesigner(models.Model):
    merchant=models.ForeignKey(Merchant,on_delete=models.PROTECT)
    designer=models.ForeignKey(Designer,on_delete=models.PROTECT)
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.IntegerField(default=1)
    amount=models.IntegerField(default=0)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.designer.name
