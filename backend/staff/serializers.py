# staff/serializers.py
from rest_framework import serializers
from .models import Role, Staff, ShiftType, WorkSchedule
from utils.date_utils import get_weekday_jp


class RoleSerializer(serializers.ModelSerializer):
    """職種シリアライザー"""

    class Meta:
        model = Role
        fields = ["id", "name"]


class StaffSerializer(serializers.ModelSerializer):
    """スタッフ情報シリアライザー"""

    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source="role", write_only=True
    )

    class Meta:
        model = Staff
        fields = ["id", "full_name", "role", "role_id", "notes"]

    def validate_full_name(self, value):
        """氏名のバリデーション：空欄禁止"""
        if not value.strip():
            raise serializers.ValidationError("氏名を入力してください。")
        return value


class ShiftTypeSerializer(serializers.ModelSerializer):
    """シフト種類シリアライザー"""

    work_hours = serializers.SerializerMethodField()

    class Meta:
        model = ShiftType
        fields = [
            "id",
            "code",
            "name",
            "start_time",
            "end_time",
            "break_minutes",
            "work_hours",
            "color",
        ]

    def get_work_hours(self, obj):
        return round(obj.get_work_duration().total_seconds() / 3600, 2)

    def validate_code(self, value):
        """コードのバリデーション：空欄禁止＆英数字"""
        if not value.strip():
            raise serializers.ValidationError("シフトコードは必須です。")
        if not value.isalnum():
            raise serializers.ValidationError("シフトコードは英数字で入力してください。")
        return value

    def validate_break_minutes(self, value):
        """休憩時間のバリデーション：0以上"""
        if value < 0:
            raise serializers.ValidationError("休憩時間は0分以上にしてください。")
        return value


class WorkScheduleSerializer(serializers.ModelSerializer):
    """勤務シフトシリアライザー"""

    staff = StaffSerializer(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), source="staff", write_only=True
    )
    shift = ShiftTypeSerializer(read_only=True)
    shift_id = serializers.PrimaryKeyRelatedField(
        queryset=ShiftType.objects.all(), source="shift", write_only=True
    )
    weekday = serializers.SerializerMethodField()

    class Meta:
        model = WorkSchedule
        fields = [
            "id",
            "staff",
            "staff_id",
            "shift",
            "shift_id",
            "date",
            "note",
            "weekday",
        ]

    def get_weekday(self, obj):
        """曜日を日本語で返す"""
        return get_weekday_jp(obj.date)

    def validate_date(self, value):
        """過去日付は登録不可"""
        from datetime import date

        if value < date.today():
            raise serializers.ValidationError("過去の日付は指定できません。")
        return value
