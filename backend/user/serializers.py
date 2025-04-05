from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    ユーザー情報をシリアライズするための基本的なシリアライザ。
    - 一般的にログイン中のユーザー情報の取得や表示に使用。
    """

    class Meta:
        model = User
        fields = ["id", "name", "email", "is_admin"]


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    ユーザー登録用のシリアライザ。
    - 管理者による新規登録や、公開登録エンドポイントに使用される。
    - パスワードは write_only として定義し、レスポンスには含まれないようにする。
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["name", "email", "password", "is_admin"]

    def create(self, validated_data):
        """
        バリデーション済みデータからユーザーを作成。
        - create_user メソッドでパスワードは自動でハッシュ化される。
        - is_admin が True の場合、同時に is_staff も True に設定する。
        """
        return User.objects.create_user(
            name=validated_data["name"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            is_admin=validated_data.get("is_admin", False),
            is_staff=validated_data.get("is_admin", False),
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWTログイン時に、トークンだけでなくユーザー情報も一緒に返すための
    カスタムシリアライザ。
    - 通常の TokenObtainPairSerializer を拡張して使用。
    """

    def validate(self, attrs):
        # デフォルトのトークン取得処理を実行
        data = super().validate(attrs)
        # トークンの他に、ログインユーザーの基本情報を追加
        data["user"] = {
            "id": self.user.id,
            "name": self.user.name,
            "email": self.user.email,
            "is_admin": self.user.is_admin,
        }
        return data
    def validate(self, attrs):
        print("JWT LOGIN DEBUG:", attrs)
        return super().validate(attrs)