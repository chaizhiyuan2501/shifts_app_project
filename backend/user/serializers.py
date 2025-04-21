from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    ユーザー登録用のシリアライザ。
    - 名前の重複チェック
    - パスワードの強度チェック
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
        """
        重複していない名前かチェック。
        """
        if User.objects.filter(name=value).exists():
            raise serializers.ValidationError("この名前は既に使用されています。")
        return value

    def validate_email(self, value):
        """
        メールアドレスがあれば、既存の登録と重複していないかチェック。
        """
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "このメールアドレスは既に登録されています。"
            )
        return value

    def validate_password(self, value):
        """
        パスワードの最低限の長さと強度をチェック。
        """
        if len(value) < 4:
            raise serializers.ValidationError(
                "パスワードは4文字以上である必要があります。"
            )
        return value

    class Meta:
        model = User
        fields = ("name", "password", "is_admin")

    def create(self, validated_data):
        """
        ユーザーを作成（パスワードをハッシュ化）。
        is_admin=Trueの場合、自動的にis_staffもTrueに。
        """
        return User.objects.create_user(**validated_data)
        # return User.objects.create_user(
        #     name=validated_data["name"],
        #     email=validated_data.get("email"),
        #     password=validated_data["password"],
        #     is_admin=validated_data.get("is_admin", False),
        #     is_staff=validated_data.get("is_admin", False),
        # )


class UserSerializer(serializers.ModelSerializer):
    """
    ユーザー情報取得・更新用のシリアライザ。
    """

    class Meta:
        model = User
        fields = ["id", "name", "email", "is_admin", "is_active"]

    def validate_name(self, value):
        """
        他のユーザーと重複していない名前かをチェック（更新用）。
        """
        if self.instance:
            if User.objects.exclude(id=self.instance.id).filter(name=value).exists():
                raise serializers.ValidationError("この名前は既に使用されています。")
        return value

    def validate_email(self, value):
        """
        他のユーザーと重複していないメールアドレスかチェック。
        """
        if value and self.instance:
            if User.objects.exclude(id=self.instance.id).filter(email=value).exists():
                raise serializers.ValidationError(
                    "このメールアドレスは既に使用されています。"
                )
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT ログイン用カスタムシリアライザ。
    ユーザー情報を含めてトークンを返す。
    """

    def validate(self, attrs):
        print("JWT LOGIN DEBUG:", attrs)  # デバッグ用
        try:
            data = super().validate(attrs)
        except Exception:
            raise serializers.ValidationError("認証情報が正しくありません。")

        data["user"] = {
            "id": self.user.id,
            "name": self.user.name,
            "email": self.user.email,
            "is_admin": self.user.is_admin,
        }
        return data
