from rest_framework import serializers
from .models import Guest, VisitType, VisitSchedule
from utils.date_utils import get_weekday_jp
from django.utils import timezone


class GuestSerializer(serializers.ModelSerializer):
    """
    Guest モデルのシリアライザ
    - 利用者情報のバリデーションと保存用
    """

    class Meta:
        model = Guest
        fields = ["id", "name", "birthday", "contact", "notes"]

    def validate_name(self, value):
        """
        氏名のバリデーション
        - 空文字や50文字超過をエラーとする
        """
        if not value.strip():
            raise serializers.ValidationError("氏名は必須です。")
        if len(value) > 50:
            raise serializers.ValidationError("氏名は50文字以内で入力してください。")
        return value

    def validate_contact(self, value):
        """
        連絡先のバリデーション
        - 5文字未満の短すぎる連絡先をエラーとする
        """
        if value and len(value) < 5:
            raise serializers.ValidationError("連絡先が短すぎます。")
        return value


class VisitTypeSerializer(serializers.ModelSerializer):
    """
    VisitType モデルのシリアライザ
    - コードと名称のバリデーションを行う
    """

    class Meta:
        model = VisitType
        fields = ["id", "code", "name", "color"]

    def validate_code(self, value):
        """
        コードのバリデーション
        - 許可された値（泊、通い、休）のみを受け付ける
        """
        allowed = ["泊", "通い", "休"]
        if value not in allowed:
            raise serializers.ValidationError(
                f"コードは {', '.join(allowed)} のいずれかにしてください。"
            )
        return value

    def validate_name(self, value):
        """
        名称のバリデーション
        - 空文字は許可しない
        """
        if not value.strip():
            raise serializers.ValidationError("来訪種別の名称は必須です。")
        return value


class VisitScheduleSerializer(serializers.ModelSerializer):
    """
    VisitSchedule モデルのシリアライザ
    - 関連モデルをIDで受け取り、オブジェクトとして返す
    - 曜日も取得可能
    - 来所時間と帰宅時間の整合性を検証
    """

    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=Guest.objects.all(), source="guest", write_only=True
    )
    visit_type_id = serializers.PrimaryKeyRelatedField(
        queryset=VisitType.objects.all(), source="visit_type", write_only=True
    )
    guest = GuestSerializer(read_only=True)
    visit_type = VisitTypeSerializer(read_only=True)
    weekday = serializers.SerializerMethodField()
    needs_breakfast = serializers.BooleanField(required=False)
    needs_lunch = serializers.BooleanField(required=False)
    needs_dinner = serializers.BooleanField(required=False)
    meal_note = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = VisitSchedule
        fields = [
            "id",
            "guest",
            "guest_id",
            "visit_type",
            "visit_type_id",
            "date",
            "arrive_time",
            "leave_time",
            "note",
            "weekday",
            "needs_breakfast",
            "needs_lunch",
            "needs_dinner",
            "meal_note",
        ]

    def get_weekday(self, obj):
        """
        曜日（日本語）の取得
        """
        return get_weekday_jp(obj.date)

    # def validate_date(self, value):
    #     """
    #     日付のバリデーション
    #     - 未来日付は禁止
    #     """
    #     if value > timezone.now().date():
    #         raise serializers.ValidationError("未来の日付は登録できません。")
    #     return value

    def validate(self, attrs):
        """
        来所時間と帰宅時間の整合性チェック
        - どちらかのみ入力された場合、または来所 > 帰宅の順序エラーを検出
        """
        arrive = attrs.get("arrive_time")
        leave = attrs.get("leave_time")
        if arrive and leave and arrive > leave:
            raise serializers.ValidationError(
                "来所時間は帰宅時間より前でなければなりません。"
            )
        return attrs


class ScheduleUploadSerializer(serializers.Serializer):
    """
    スケジュール画像アップロード用シリアライザ
    - 最大5MBの画像サイズ制限あり
    """

    image = serializers.ImageField()

    def validate_image(self, value):
        """
        アップロード画像のサイズ検証
        """
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "画像サイズが大きすぎます（最大5MBまで）。"
            )
        return value
