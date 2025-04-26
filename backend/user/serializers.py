from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    ユーザー新規登録用シリアライザ。
    - 名前・パスワード必須
    - 重複チェック・パスワードバリデーションあり
    """

    name = serializers.CharField(
        label="表示名",
        max_length=255,
        min_length=2,
        help_text="2文字以上の名前を入力してください",
    )
    password = serializers.CharField(
        write_only=True,
        min_length=4,
        help_text="4文字以上のパスワードを入力してください",
    )

    class Meta:
        model = User
        fields = ["name", "email", "password", "is_admin"]

    def validate_name(self, value):
        """名前の重複をチェック"""
        if User.objects.filter(name=value).exists():
            raise serializers.ValidationError("この名前は既に使用されています。")
        return value

    def validate_email(self, value):
        """メールアドレスの重複をチェック"""
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "このメールアドレスは既に登録されています。"
            )
        return value

    def validate_password(self, value):
        """パスワードの長さチェック"""
        if len(value) < 4:
            raise serializers.ValidationError(
                "パスワードは4文字以上である必要があります。"
            )
        return value

    def create(self, validated_data):
        """ユーザー作成処理（パスワードハッシュ化済）"""
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    ユーザー情報取得・更新用シリアライザ。
    """

    class Meta:
        model = User
        fields = ["id", "name", "email", "is_admin", "is_active"]

    def validate_name(self, value):
        """名前変更時の重複チェック"""
        if self.instance:
            if User.objects.exclude(id=self.instance.id).filter(name=value).exists():
                raise serializers.ValidationError("この名前は既に使用されています。")
        return value

    def validate_email(self, value):
        """メールアドレス変更時の重複チェック"""
        if value and self.instance:
            if User.objects.exclude(id=self.instance.id).filter(email=value).exists():
                raise serializers.ValidationError(
                    "このメールアドレスは既に使用されています。"
                )
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT認証用カスタムシリアライザ。
    - ログイン時にユーザー情報も一緒に返す
    """

    def validate(self, attrs):
        print("JWT LOGIN DEBUG:", attrs)  # デバッグ用
        try:
            data = super().validate(attrs)
        except Exception:
            raise serializers.ValidationError("認証情報が正しくありません。")

        # 成功時、ユーザー情報も追加する
        data["user"] = {
            "id": self.user.id,
            "name": self.user.name,
            "email": self.user.email,
            "is_admin": self.user.is_admin,
        }
        return data
