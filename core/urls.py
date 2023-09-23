from django.urls import path,include
from .views import * 

urlpatterns = [
    path('check/phoneno/',PhoneNumberExists.as_view()),
    path('designer/',DesignerAPI.as_view()),
    path('designer/profile/',DesignerView.as_view()),
    path('merchant/',MerchantAPI.as_view()),
    path('merchant/profile/',MerchantView.as_view()),

]