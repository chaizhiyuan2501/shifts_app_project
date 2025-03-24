from rest_framework import serializers
from .models import Guest, VisitType, GuestVisitSchedule
from django.contrib.auth.models import User
from .models import Guest, VisitType


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
            "arrive_time",
            "leave_time",
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

    class Meta:
        model = GuestVisitSchedule
        fields = [
            "id",
            "guest",
            "date",
            "visit_type",
            "note",
        ]
