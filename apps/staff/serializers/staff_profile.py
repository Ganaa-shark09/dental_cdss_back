from rest_framework import serializers

from apps.clinics.models import Clinic
from apps.staff.models import StaffProfile
from apps.users.models import User


class StaffProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    clinic_name = serializers.CharField(source="clinic.name", read_only=True)

    class Meta:
        model = StaffProfile
        fields = (
            "uuid",
            "user",
            "user_name",
            "user_email",
            "clinic",
            "clinic_name",
            "employee_id",
            "designation",
            "specialization",
            "license_number",
            "years_of_experience",
            "is_active",
            "created_at",
            "updated_at",
        )


class StaffProfileCreateSerializer(serializers.Serializer):
    user = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=User.objects.filter(is_active=True),
    )
    clinic = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Clinic.objects.filter(is_active=True),
    )
    designation = serializers.CharField(max_length=100)
    specialization = serializers.CharField(
        max_length=150, required=False, allow_blank=True
    )
    license_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    years_of_experience = serializers.IntegerField(
        required=False, default=0, min_value=0
    )
    is_active = serializers.BooleanField(required=False, default=True)


class StaffProfileUpdateSerializer(serializers.Serializer):
    clinic = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Clinic.objects.filter(is_active=True),
        required=False,
    )
    designation = serializers.CharField(max_length=100, required=False)
    specialization = serializers.CharField(
        max_length=150, required=False, allow_blank=True
    )
    license_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    years_of_experience = serializers.IntegerField(required=False, min_value=0)
    is_active = serializers.BooleanField(required=False)
