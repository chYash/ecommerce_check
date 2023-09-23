from django.shortcuts import render
from rest_framework.views import APIView

from . import models, serializers
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from django.core.exceptions import ObjectDoesNotExist
from product import models as productmodels


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class PhoneNumberExists(APIView):

    queryset = models.User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self,request):

        try:
            queryset=models.User.objects.get(phone=request.data["phone"])
        except ObjectDoesNotExist:
            return Response({"msg":"Phone number does not exist."}, status=200)
        return Response({"msg":"Phone number exists."},status=400)
            

class DesignerAPI(generics.CreateAPIView):

    queryset = models.Designer.objects.all()
    serializer_class = serializers.DesignerSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request,*args,**kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = self.queryset.get(id=serializer.data["id"])
        follow = models.Followers.objects.create(designer=instance)
        return Response(serializer.data,status=200)


class DesignerView(generics.RetrieveUpdateAPIView):
    queryset = models.Designer.objects.all()
    serializer_class = serializers.DesignerSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def retrieve(self, request,*args,**kwargs):

        if not request.user.is_designer:
            return Response({"error":"User is not a designer"},status=200)

        designer = self.queryset.get(user=request.user)

        serializer = self.get_serializer(designer)

        return Response(serializer.data,status=200)

    def partial_update(self, request,*args,**kwargs):

        if not request.user.is_designer:
            return Response({"error":"User is not a designer"},status=200)

        designer = self.queryset.get(user=request.user)
        serializer = self.get_serializer(designer,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=200)

class MerchantAPI(generics.CreateAPIView):

    queryset = models.Merchant.objects.all()
    serializer_class = serializers.MerchantSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request,*args,**kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = self.queryset.get(id=serializer.data["id"])
        follow = models.Following.objects.create(merchant=instance)
        home = productmodels.MerchantHomeProduct.objects.create(merchant=instance)
        return Response(serializer.data,status=200)


class MerchantView(generics.RetrieveUpdateAPIView):
    queryset = models.Merchant.objects.all()
    serializer_class = serializers.MerchantSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def retrieve(self, request,*args,**kwargs):

        if not request.user.is_merchant:
            return Response({"error":"User is not a merchant"},status=200)

        merchant = self.queryset.get(user=request.user)

        serializer = self.get_serializer(merchant)

        return Response(serializer.data,status=200)

    def partial_update(self, request,*args,**kwargs):

        if not request.user.is_merchant:
            return Response({"error":"User is not a merchant"},status=200)

        merchant = self.queryset.get(user=request.user)
        serializer = self.get_serializer(merchant,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=200)


class Notification(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializers.NotificationSerializer
    def get_queryset(self):
        user = self.request.user
        query_set=models.Notification.objects.filter(user=user).order_by('-noti_id')
        return query_set

