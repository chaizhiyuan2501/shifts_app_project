from rest_framework import serializers
import datetime

from .models import MealType, MealOrder
from guest.models import Guest
from staff.models import Staff

from utils.date_utils import get_weekday_jp


class MealTypeSerializer(serializers.ModelSerializer):
    """食事種類のシリアライザー"""

    class Meta:
        model = MealType
        fields = ["id", "name", "display_name"]


class GuestMealOrderSerializer(serializers.ModelSerializer):
    """ゲスト用の食事注文シリアライザー"""

    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=Guest.objects.all(), source="guest"
    )
    meal_type = MealTypeSerializer(read_only=True)
    meal_type_id = serializers.PrimaryKeyRelatedField(
        queryset=MealType.objects.all(), source="meal_type", write_only=True
    )
    weekday = serializers.SerializerMethodField()

    class Meta:
        model = MealOrder
        fields = [
            "id",
            "date",
            "meal_type",
            "meal_type_id",
            "guest",
            "guest_id",
            "ordered",
            "auto_generated",
            "note",
            "weekday",
        ]

    def get_weekday(self, obj):
        return get_weekday_jp(obj.date)

    def validate_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError("過去の日付は選択できません。")
        return value

    def get_serializer_class(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, "staff"):
                return StaffMealOrderSerializer
            elif hasattr(request.user, "guest"):
                return GuestMealOrderSerializer
        return GuestMealOrderSerializer

    def validate(self, attrs):
        date = attrs.get("date")
        meal_type = attrs.get("meal_type")
        guest = attrs.get("guest")

        if MealOrder.objects.filter(
            date=date, meal_type=meal_type, guest=guest
        ).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["既にこのゲストの注文が存在します。"]}
            )
        return attrs


class StaffMealOrderSerializer(serializers.ModelSerializer):
    """スタッフ用の食事注文シリアライザー"""

    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), source="staff"
    )
    meal_type = MealTypeSerializer(read_only=True)
    meal_type_id = serializers.PrimaryKeyRelatedField(
        queryset=MealType.objects.all(), source="meal_type", write_only=True
    )
    weekday = serializers.SerializerMethodField()

    class Meta:
        model = MealOrder
        fields = [
            "id",
            "date",
            "meal_type",
            "meal_type_id",
            "staff",
            "staff_id",
            "ordered",
            "auto_generated",
            "note",
            "weekday",
        ]

    def get_weekday(self, obj):
        return get_weekday_jp(obj.date)

    def validate_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError("過去の日付は選択できません。")
        return value

    def get_serializer_class(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, "staff"):
                return StaffMealOrderSerializer
            elif hasattr(request.user, "guest"):
                return GuestMealOrderSerializer
        return GuestMealOrderSerializer

    def validate(self, attrs):
        date = attrs.get("date")
        meal_type = attrs.get("meal_type")
        staff = attrs.get("staff")

        if MealOrder.objects.filter(
            date=date, meal_type=meal_type, staff=staff
        ).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["既にこのスタッフの注文が存在します。"]}
            )
        return attrs
