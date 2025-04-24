from rest_framework import serializers
import datetime

from .models import MealType, MealOrder
from guest.models import Guest
from staff.models import Staff

from utils.date_utils import get_weekday_jp


class MealTypeSerializer(serializers.ModelSerializer):
    """
    食事種類のシリアライザー
    - MealType モデルの情報（id, コード, 表示名）を提供
    """

    class Meta:
        model = MealType
        fields = ["id", "name", "display_name"]


class GuestMealOrderSerializer(serializers.ModelSerializer):
    """
    ゲスト用の食事注文シリアライザー
    - 食事タイプとゲスト情報を含み、注文データを管理
    """

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
        """
        日付から曜日（日本語）を返す補助メソッド
        """
        return get_weekday_jp(obj.date)

    # def validate_date(self, value):
    #     """
    #     日付のバリデーション
    #     - 過去の日付は選択不可（未来の注文のみ登録可能）
    #     - 昨日以前の注文登録を防ぐ
    #     """
    #     if value < datetime.date.today():
    #         raise serializers.ValidationError("過去の日付は選択できません。")
    #     return value

    def validate(self, attrs):
        """
        重複注文のチェック
        - 同一日付・食事種別・ゲストで既に存在する場合はエラー
        """
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
    """
    スタッフ用の食事注文シリアライザー
    - スタッフごとの注文情報を管理
    """

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
        """
        日付に対する曜日（日本語）を取得する
        """
        return get_weekday_jp(obj.date)

    def validate_date(self, value):
        """
        日付のバリデーション
        - 過去日付は選択不可（スタッフも未来分のみ登録可）
        """
        if value < datetime.date.today():
            raise serializers.ValidationError("過去の日付は選択できません。")
        return value

    def validate(self, attrs):
        """
        重複注文のチェック
        - 同じ日・食事タイプ・スタッフの組み合わせで注文が既にある場合はエラー
        """
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
