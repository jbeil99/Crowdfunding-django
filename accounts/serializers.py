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


class UserProfileSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["id", "email", "created_at"]

    def get_profile_picture(self, obj):
        request = self.context.get("request")
        if request:
            try:
                obj.profile_picture.url
            except ValueError:
                return None
            return request.build_absolute_uri(obj.profile_picture.url)
        return obj.profile_picture.url

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long."
            )
        return value

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name is required.")
        return value

    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Last name is required.")
        return value

    def validate_mobile_phone(self, value):
        egyptian_pattern = r"^01[0125][0-9]{8}$"
        if not re.match(egyptian_pattern, value):
            raise serializers.ValidationError("Enter a valid Egyptian mobile number.")
        return value

    def validate_facebook(self, value):
        if value and not value.startswith("https://www.facebook.com/"):
            raise serializers.ValidationError(
                "Facebook URL must start with https://www.facebook.com/"
            )
        return value

    def validate_country(self, value):
        if value and not value.strip():
            raise serializers.ValidationError("Country must not be blank.")
        return value
