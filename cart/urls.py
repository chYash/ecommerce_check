from django.urls import path,include
from .views import *


urlpatterns = [
    path('add-savedproduct/',SavedProductView.as_view()),
    path('remove-savedproduct/',RemoveSavedProductView.as_view()),
    path('cart/',CartView.as_view()),
    path('add-to-cart/',AddtoCartView.as_view()),
    path('remove-from-cart/',RemovefromCartView.as_view()),
    path('confirm-payment/',ConfirmPaymentAPIView.as_view()),
    path('past-orders/',PastOrderView.as_view()),
    path('past-orders/<int:id>/',OrderedItems.as_view()),
    # path('items/',ItemsAPIView.as_view()),
    # path('addtocart/',AddtoCartAPIView.as_view()),
    # path('removefromcart/',RemovefromCartAPIView.as_view()),
    # path('confirmpayment/',ConfirmPaymentAPIView.as_view()),
    # path('pastorders/',PastOrdersAPIView.as_view()),
    # path('getbill/',BillView.as_view()),
    # path('recent/',RecentOrdersListAPIView.as_view()),
    # path('totalrevenue/',TotalRevenueAPIView.as_view()),
    # path('monthlyrevenue/',MonthlyRevenueAPIView.as_view()),
]