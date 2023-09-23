from django.db import models
from core.models import User,Designer,Merchant
from django.utils.text import slugify
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

class Subcategory(models.Model):

    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    designer = models.ForeignKey(Designer, on_delete=models.PROTECT)
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    sub_category = models.ForeignKey("Subcategory", on_delete=models.PROTECT)
    name = models.CharField(max_length=126)
    code = models.CharField(unique=True,max_length=50)
    area = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    stitch = models.IntegerField(default=0)
    needle = models.IntegerField(default=0)
    machine = models.CharField(max_length=50, default="None")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    image1 = models.ImageField(upload_to="product/",blank=True,null=True)
    image2 = models.ImageField(upload_to="product/", blank=True,null=True)
    image3 = models.ImageField(upload_to="product/", blank=True,null=True)
    image4 = models.ImageField(upload_to="product/", blank=True,null=True)
    price=models.IntegerField(default=0)
    file = models.FileField()

    def __str__(self):
        return str(self.id)+" "+self.name

class MerchantHomeProduct(models.Model):
    merchant = models.ForeignKey('core.Merchant',on_delete=models.PROTECT)
    product = models.ManyToManyField('Product')

    def __str__(self):
        return self.merchant.name

@receiver(pre_save, sender=Category)
def slugify_name2(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)

@receiver(pre_save, sender=Subcategory)
def slugify_name(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)

# class Orders(models.Model):
#     bill_id = models.AutoField(primary_key=True)
#     bill_amount = models.FloatField(default=0)
#     buyer_name = models.CharField(max_length=50, default="Unknown")
#     date_of_purchase = models.DateField(default=datetime.datetime.now().date())
#     time_of_purchase = models.TimeField(default=datetime.datetime.now().time())
#     user_id = models.ForeignKey(Merchant, on_delete=models.CASCADE, null=True)
#     def __str__(self):
#         return self.bill_id;
#
# class Cart(models.Model):
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     product_quantity = models.IntegerField(default=0)
#     total_amount = models.FloatField(default=0)
#
# class Order_Product(models.Model):
#     bill_id = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True)
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     quantity = models.IntegerField(default=0)

