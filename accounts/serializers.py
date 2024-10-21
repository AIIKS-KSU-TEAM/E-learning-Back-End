from rest_framework import serializers
from accounts.models import Teacher
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["access_token"] = data.pop("access")
        data["refresh_token"] = data.pop("refresh")

        # Add token type
        data["token_type"] = "Bearer"

        # Calculate the expiration time for the access token in seconds
        data["expires_in"] = int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds())

        return data


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
