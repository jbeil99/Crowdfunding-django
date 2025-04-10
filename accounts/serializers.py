from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer as BaseUserSerializer,
)

User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    mobile_phone = serializers.CharField(required=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            "mobile_phone",
            "profile_picture",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "password": {"write_only": True},
        }

    def validate_mobile_phone(self, value):
        print("Validating mobile phone...")
        pattern = r"^01[0125]\d{8}$"
        value = str(value).strip()

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Invalid Egyptian phone number. Must be 11 digits starting with 010, 011, 012, or 015"
            )
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(
                {"confirm_password": "Passwords don't match"}
            )
        return attrs


class UserSerializer(BaseUserSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "mobile_phone",
            "profile_picture",
            "created_at",
        ]
        read_only_fields = ["id", "email"]

    def get_profile_picture(self, obj):
        request = self.context.get("request")
        if request:
            try:
                obj.profile_picture.url
            except ValueError:
                return None

            return request.build_absolute_uri(obj.profile_picture.url)
        return obj.profile_picture.url


class UserProfileSerializer(BaseUserSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "mobile_phone",
            "profile_picture",
            "date_of_birth",
            "facebook",
            "country",
            "created_at",
        ]
        read_only_fields = ["id", "email"]

    def get_profile_picture(self, obj):
        request = self.context.get("request")
        if request:
            try:
                obj.profile_picture.url
            except ValueError:
                return None

            return request.build_absolute_uri(obj.profile_picture.url)
        return obj.profile_picture.url
