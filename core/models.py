from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone Number must be entered in the format: '+999999999'. Upto 14 digits allowed.")
    phone=models.CharField(validators=[phone_regex],max_length=15, unique=True )
    is_designer=models.BooleanField(default=False)
    is_merchant=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    
gender_choices= (
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other"),
)

class Designer(models.Model):
    user=models.ForeignKey('User',on_delete=models.PROTECT)
    name=models.CharField(max_length=200,default="")
    gender=models.CharField(max_length=10,choices=gender_choices)
    phone=models.CharField(max_length=10,default="")
    email = models.EmailField(default="")
    machine=models.CharField(max_length=200,default="")
    design_category=models.CharField(max_length=200,default="")
    image=models.ImageField(upload_to="designer/",blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Merchant(models.Model):
    user=models.ForeignKey('User',on_delete=models.PROTECT)
    name=models.CharField(max_length=200,default="")
    gender=models.CharField(max_length=10,choices=gender_choices)
    phone=models.CharField(max_length=10,default="")
    email = models.EmailField(default="")
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    image=models.ImageField(blank=True,null=True)

    def __str__(self):
        return self.name


class Enquiry(models.Model):
    name = models.CharField(max_length=126)
    email = models.EmailField(max_length=126)
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone Number must be entered in the format: '+999999999'. Upto 14 digits allowed.")
    phone=models.CharField(validators=[phone_regex],max_length=15)
    enquiry = models.TextField()

    def __str__(self):
        return self.name

class Followers(models.Model):
    designer= models.OneToOneField('Designer',on_delete=models.PROTECT,primary_key=True)
    followers_id = models.ManyToManyField(Merchant)

    def __str__(self):
        return self.designer.name

class Following(models.Model):
    merchant = models.OneToOneField('Merchant',on_delete=models.PROTECT,primary_key=True)
    following_id = models.ManyToManyField(Designer)

    def __str__(self):
        return self.merchant.name


class Notification(models.Model):
    user=models.ForeignKey('User',on_delete=models.PROTECT)
    title=models.CharField(max_length=200,default="")
    Description = models.CharField(max_length=10000,default="")
    created = models.DateTimeField(auto_now_add=True)



# class UserNotification(models.Model):
#     noti_id = models.ManyToManyField(Notification);
#     user = models.OneToOneField(User)
