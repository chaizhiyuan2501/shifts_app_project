from rest_framework import serializers
from datetime import datetime

from .models import MealType, MealOrder
from guest.models import Guest
from staff.models import Staff

from utils.date_utils import get_weekday_jp


class MealTypeSerializer(serializers.ModelSerializer):
    """食事種類のシリアライザー"""

    class Meta:
        model = MealType
        fields = ["id", "name", "display_name"]


class MealOrderSerializer(serializers.ModelSerializer):
    """食事注文シリアライザー"""

    # 読み取り専用の食事タイプ情報（詳細表示用）
    meal_type = MealTypeSerializer(read_only=True)

    # 書き込み専用の食事タイプID
    meal_type_id = serializers.PrimaryKeyRelatedField(
        queryset=MealType.objects.all(), source="meal_type", write_only=True
    )

    # 読み取り専用の利用者表示名
    guest = serializers.StringRelatedField(read_only=True)
    # 書き込み専用の利用者ID（nullable、任意）
    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=Guest.objects.all(),
        source="guest",
        write_only=True,
        allow_null=True,
        required=False,
    )

    # 読み取り専用のスタッフ表示名
    staff = serializers.StringRelatedField(read_only=True)
    # 書き込み専用のスタッフID（nullable、任意）
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(),
        source="staff",
        write_only=True,
        allow_null=True,
        required=False,
    )

    # 曜日（日本語）を計算して返す
    weekday = serializers.SerializerMethodField()

    class Meta:
        model = MealOrder
        fields = [
            "id",
            "date",
            "meal_type",  # 表示用
            "meal_type_id",  # 入力用
            "guest",
            "guest_id",
            "staff",
            "staff_id",
            "ordered",
            "auto_generated",
            "note",
            "weekday",
        ]

    def get_weekday(self, obj):
        """
        date フィールドから日本語の曜日を取得する
        """
        return get_weekday_jp(obj.date)

    def validate(self, data):
        """
        入力データ全体に対するバリデーション。
        - staffとguestの両方がnullでないことを保証
        - staffとguestが同時に指定されていないことをチェック
        """
        staff = data.get("staff")
        guest = data.get("guest")

        # スタッフとゲストの両方が指定されている場合はエラー
        if staff and guest:
            raise serializers.ValidationError(
                "スタッフと利用者の両方を同時に指定することはできません。"
            )

        # スタッフとゲストの両方が未指定の場合もエラー
        if not staff and not guest:
            raise serializers.ValidationError(
                "スタッフまたは利用者のいずれかを指定してください。"
            )

        return data

    def validate_date(self, value):
        """
        日付のバリデーション：
        - 過去の日付を選択できないようにする
        """
        if value < datetime.date.today():
            raise serializers.ValidationError("過去の日付は選択できません。")
        return value
