from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password', 'mobile_phone', 'profile_picture']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }
    
    def validate_mobile_phone(self, value):
        pattern = r'^(\+201|01)[0-9]{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Please enter a valid Egyptian phone number.")
        return value
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords don't match"})
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile_phone=validated_data['mobile_phone'],
            profile_picture=validated_data.get('profile_picture', None),
            is_active=False  # User is inactive until they confirm their email
        )
        return user




class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_active:
            raise serializers.ValidationError(
                {"error": "Please activate your account first."}
            )
        return data