from rest_framework import serializers
from .models import Role, Staff, ShiftType, WorkSchedule
from utils.date_utils import get_weekday_jp


class RoleSerializer(serializers.ModelSerializer):
    """職種情報をシリアライズ・デシリアライズするためのシリアライザー"""

    class Meta:
        model = Role
        fields = ["id", "name"]


class StaffSerializer(serializers.ModelSerializer):
    """スタッフ情報をシリアライズ・デシリアライズするためのシリアライザー"""

    # 読み取り専用で職種情報（RoleSerializer）をネスト表示
    role = RoleSerializer(read_only=True)
    # 書き込み時はIDで指定
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source="role", write_only=True
    )

    class Meta:
        model = Staff
        fields = ["id", "name", "role", "role_id", "notes"]

    def create(self, validated_data):
        """
        スタッフ登録時に、userフィールドが指定されていない場合、
        ログイン中ユーザーを自動的に割り当てる。
        """
        if "user" not in validated_data and self.context.get("request"):
            validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate_name(self, value):
        """氏名バリデーション：空欄禁止"""
        if not value.strip():
            raise serializers.ValidationError("氏名を入力してください。")
        return value


class ShiftTypeSerializer(serializers.ModelSerializer):
    """シフト種類（早番・遅番・夜勤など）をシリアライズ・デシリアライズするシリアライザー"""

    # 勤務時間（休憩時間除く）を自動計算して返すフィールド
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
        """
        シフトの実働時間（時間単位）を計算して返す。
        """
        return round(obj.get_work_duration().total_seconds() / 3600, 2)

    def validate_code(self, value):
        """コードバリデーション：空欄禁止＆英数字のみ許可"""
        if not value.strip():
            raise serializers.ValidationError("シフトコードは必須です。")
        if not value.isalnum():
            raise serializers.ValidationError(
                "シフトコードは英数字で入力してください。"
            )
        return value

    def validate_break_minutes(self, value):
        """休憩時間バリデーション：0分以上に制限"""
        if value < 0:
            raise serializers.ValidationError("休憩時間は0分以上にしてください。")
        return value


class WorkScheduleSerializer(serializers.ModelSerializer):
    """勤務シフト情報をシリアライズ・デシリアライズするためのシリアライザー"""

    # スタッフ情報とシフト情報は読み取り時に詳細表示
    staff = StaffSerializer(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), source="staff", write_only=True
    )
    shift = ShiftTypeSerializer(read_only=True)
    shift_id = serializers.PrimaryKeyRelatedField(
        queryset=ShiftType.objects.all(), source="shift", write_only=True
    )
    # 曜日を日本語表記で返す
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
        """日付に対応する日本語の曜日を返す"""
        return get_weekday_jp(obj.date)

    def validate_date(self, value):
        """勤務日のバリデーション：過去日付は禁止"""
        from datetime import date

        if value < date.today():
            raise serializers.ValidationError("過去の日付は指定できません。")
        return value
