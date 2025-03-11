from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers

import re


class UserSerializer(serializers.ModelSerializer):
    """ユーザーオブジェクトのシリアライザー"""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """パスワードを暗号化してユーザーを作成する"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ユーザー情報を更新する"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """ユーザー認証トークンのシリアライザー。"""

    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=True,  # パスワードの空白を削除する
    )

    def validate(self, attrs):
        """ユーザーを検証し、認証します。"""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            msg = _("提供された情報で認証できません。")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
