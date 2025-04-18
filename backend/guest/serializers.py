from rest_framework import serializers
from .models import Guest, VisitType, VisitSchedule
from utils.date_utils import get_weekday_jp
from django.utils import timezone


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ["id", "name", "birthday", "contact", "notes"]

    def validate_name(self, value):
        """氏名が空でないかチェック"""
        if not value.strip():
            raise serializers.ValidationError("氏名は必須です。")
        if len(value) > 50:
            raise serializers.ValidationError("氏名は50文字以内で入力してください。")
        return value

    def validate_contact(self, value):
        """連絡先の簡易フォーマットチェック"""
        if value and len(value) < 5:
            raise serializers.ValidationError("連絡先が短すぎます。")
        return value


class VisitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitType
        fields = ["id", "code", "name", "color"]

    def validate_code(self, value):
        """コードは泊・通い・休のいずれかのみ許可"""
        allowed = ["泊", "通い", "休"]
        if value not in allowed:
            raise serializers.ValidationError(
                f"コードは {', '.join(allowed)} のいずれかにしてください。"
            )
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("来訪種別の名称は必須です。")
        return value


class VisitScheduleSerializer(serializers.ModelSerializer):
    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=Guest.objects.all(), source="guest", write_only=True
    )
    visit_type_id = serializers.PrimaryKeyRelatedField(
        queryset=VisitType.objects.all(), source="visit_type", write_only=True
    )
    guest = GuestSerializer(read_only=True)
    visit_type = VisitTypeSerializer(read_only=True)
    weekday = serializers.SerializerMethodField()

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
        ]

    def get_weekday(self, obj):
        """曜日の日本語を返す"""
        return get_weekday_jp(obj.date)

    def validate_date(self, value):
        """未来の日付は登録不可"""
        if value > timezone.now().date():
            raise serializers.ValidationError("未来の日付は登録できません。")
        return value

    def validate(self, attrs):
        """
        来所時間と帰宅時間の整合性をチェック（どちらかのみ存在、または順序逆転は不可）
        """
        arrive = attrs.get("arrive_time")
        leave = attrs.get("leave_time")
        if arrive and leave and arrive > leave:
            raise serializers.ValidationError(
                "来所時間は帰宅時間より前でなければなりません。"
            )
        return attrs


class ScheduleUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, value):
        """画像ファイルの簡易検証"""
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "画像サイズが大きすぎます（最大5MBまで）。"
            )
        return value
