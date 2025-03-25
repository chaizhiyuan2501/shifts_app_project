from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """ユーザー情報表示用"""

    class Meta:
        model = User
        fields = ["id", "name", "email", "is_admin"]


class RegisterUserSerializer(serializers.ModelSerializer):
    """ユーザー登録用"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["name", "email", "password", "is_admin"]

    def create(self, validated_data):
        return User.objects.create_user(
            name=validated_data["name"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            is_admin=validated_data.get("is_admin", False),
            is_staff=validated_data.get("is_admin", False),
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWTログイン時にユーザー情報も一緒に返す
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "name": self.user.name,
            "email": self.user.email,
            "is_admin": self.user.is_admin,
        }
        return data
