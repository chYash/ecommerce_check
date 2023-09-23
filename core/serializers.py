from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from . import models
from django.core.validators import RegexValidator


class CoreRegisterSerializer(RegisterSerializer):

    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone Number must be entered in the format: '+999999999'. Upto 14 digits allowed.")
    phone=serializers.CharField(validators=[phone_regex],max_length=15)
    is_designer=serializers.BooleanField(default=False)
    is_merchant=serializers.BooleanField(default=False)
    is_admin=serializers.BooleanField(default=False)


    class Meta:
        model = models.User
        fields = ('email', 'username', 'password','phone', 'is_designer', 'is_merchant', 'is_admin')


    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', ''),
            'is_designer': self.validated_data.get('is_designer', ''),
            'is_merchant': self.validated_data.get('is_merchant', ''),
            'is_admin': self.validated_data.get('is_admin', ''),
        }

    def save(self,request):
        adapter=get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.phone = self.cleaned_data.get('phone')
        user.is_designer = self.cleaned_data.get('is_designer')
        user.is_merchant = self.cleaned_data.get('is_merchant')
        user.is_admin = self.cleaned_data.get('is_admin')
        user.save()
        adapter.save_user(request, user, self)
        return user

 

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('email', 'username', 'password','phone', 'is_admin', 'is_merchant', 'is_designer')

    
class TokenSerializer(serializers.ModelSerializer):

    user_type=serializers.SerializerMethodField()

    class Meta:
        model=Token
        fields = ('key','user','user_type')

    def get_user_type(self,obj):

        serializer_data = UserSerializer(
            obj.user
        ).data
        is_admin = serializer_data.get('is_admin')
        is_merchant = serializer_data.get('is_merchant')
        is_designer = serializer_data.get('is_designer')
        return {
            'is_admin': is_admin,
            'is_merchant': is_merchant,
            'is_designer': is_designer,
            
        }

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Merchant
        fields='__all__'
   
class EnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Enquiry
        fields = '__all__'



class DesignerSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.Designer
        fields='__all__'

class DesignerMinSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Designer
        fields = ["id","name","image"]

class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.Following
        fields='__all__'

class FollowersSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.Followers
        fields='__all__'

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.Notification
        fields='__all__'