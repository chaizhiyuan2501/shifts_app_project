from rest_framework import serializers
from .models import Guest, VisitType, VisitSchedule
from django.contrib.auth.models import User

from .models import Guest, VisitType
from utils.date_utils import get_weekday_jp


class GuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guest
        fields = [
            "id",
            "full_name",
            "contact",
        ]


class VisitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitType
        fields = [
            "id",
            "code",
            "name",
            "color",
        ]


class VisitScheduleSerializer(serializers.ModelSerializer):

    guest = GuestSerializer(read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=Guest.objects.all(), source="guest", write_only=True
    )
    visit = VisitTypeSerializer(read_only=True)
    visit_id = serializers.PrimaryKeyRelatedField(
        queryset=VisitType.objects.all(), source="visit", write_only=True
    )
    weekday = serializers.SerializerMethodField()

    def weekday_jp(self):
        """
        指定した日付の曜日を日本語で返す
        """
        return get_weekday_jp(self.date)

    class Meta:
        model = VisitSchedule
        fields = [
            "id",
            "guest",
            "guest_id",
            "date",
            "arrive_time",
            "leave_time",
            "visit",
            "visit_id",
            "note",
            "weekday",
        ]
