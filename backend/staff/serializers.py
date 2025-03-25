from rest_framework import serializers
from .models import Role, Staff, ShiftType, WorkSchedule


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
        fields = [
            "id",
            "full_name",
            "role",
            "role_id",
            "notes",
        ]


class ShiftTypeSerializer(serializers.ModelSerializer):
    """シフト種類シリアライザー"""

    class Meta:
        model = ShiftType
        fields = [
            "id",
            "code",
            "name",
            "start_time",
            "end_time",
            "color",
        ]


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
        ]
