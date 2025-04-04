from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
import re
from djoser.serializers import UserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserRegistrationSerializer(UserCreateSerializer):
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    mobile_phone = serializers.CharField(required=True)
    profile_picture = serializers.ImageField(required=False)
    
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password', 
                 'mobile_phone', 'profile_picture']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True},
        }
    
    def validate_mobile_phone(self, value):
        pattern = r'^(\+201|01)[0-9]{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Please enter a valid Egyptian phone number.")
        return value
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords don't match"})
        return attrs
    
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

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 
                 'mobile_phone', 'profile_picture', 'is_active']
        read_only_fields = ['id', 'email', 'is_active']

class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        user = authenticate(
            email=attrs.get('email'),
            password=attrs.get('password')
        )
        
        if not user:
            raise serializers.ValidationError({
                'detail': 'Invalid email or password.'
            })
            
        if not user.is_active:
            raise serializers.ValidationError({
                'detail': 'Account is not activated.'
            })
            
        data = super().validate(attrs)
        return data