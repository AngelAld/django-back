from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class LoginSerializer(serializers.ModelSerializer):
    tokens = TokenSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
            "tokens",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "username": {"read_only": True},
        }

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError("Credenciales invalidas")
        refresh = RefreshToken.for_user(user)

        return {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        }
