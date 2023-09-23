from django.contrib import admin
from .models import Product_saved,Cart,Items,RecentOrdersDesigner
# Register your models here.
admin.site.register(Product_saved)
admin.site.register(Cart)
admin.site.register(Items)
admin.site.register(RecentOrdersDesigner)