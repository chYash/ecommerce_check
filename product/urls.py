from django.urls import path,include
from .views import *


urlpatterns = [
    # path('allproduct/',AllProductView.as_view()),
    # path('product/',CategoryProductView.as_view()),
    # path('filter/',FilterProductAPIView.as_view()),
    # path('searchproduct/',ProductSearchAPIView.as_view()),
    path('category/',categoryViewAPI.as_view()),
    path('category/<int:id>/',categoryUpdateViewAPI.as_view()),
    path('subcategory/<slug:name>/',subcategoryslugapi.as_view()),
    path('list/<slug:cat>/<slug:sub>/',ProductListApi.as_view()),
    path('all/',AllProductsAPI.as_view()),
    path("designer/",DesignerProductList.as_view()),
    path("designer/edit/<int:id>/",DesignerProductEditApi.as_view()),


]