from rest_framework import serializers
from .models import MealType, MealOrder
from guest.models import Guest
from staff.models import Staff


class MealTypeSerializer(serializers.ModelSerializer):
    """食事種類のシリアライザー"""

    class Meta:
        model = MealType
        fields = ["id", "name", "display_name"]


class MealOrderSerializer(serializers.ModelSerializer):
    """食事注文シリアライザー"""

    meal_type = MealTypeSerializer(read_only=True)
    meal_type_id = serializers.PrimaryKeyRelatedField(
        queryset=MealType.objects.all(), source="meal_type", write_only=True
    )
    guest = serializers.StringRelatedField(read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=Guest.objects.all(),
        source="guest",
        write_only=True,
        allow_null=True,
        required=False,
    )
    staff = serializers.StringRelatedField(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(),
        source="staff",
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = MealOrder
        fields = [
            "id",
            "date",
            "meal_type",  # 输出用
            "meal_type_id",  # 输入用
            "guest",
            "guest_id",
            "staff",
            "staff_id",
            "ordered",
            "auto_generated",
            "note",
        ]
