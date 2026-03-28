from rest_framework import serializers

from apps.appointments.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    clinic_name = serializers.CharField(source="clinic.name", read_only=True)
    staff_name = serializers.CharField(
        source="staff_profile.user.full_name", read_only=True
    )

    class Meta:
        model = Appointment
        fields = (
            "uuid",
            "appointment_number",
            "patient",
            "patient_name",
            "clinic",
            "clinic_name",
            "staff_profile",
            "staff_name",
            "appointment_date",
            "appointment_time",
            "status",
            "reason_for_visit",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
        )


class AppointmentCreateSerializer(serializers.Serializer):
    patient_id = serializers.UUIDField()
    clinic_id = serializers.UUIDField()
    staff_profile_id = serializers.UUIDField(required=False, allow_null=True)
    appointment_number = serializers.CharField(max_length=50)
    appointment_date = serializers.DateField()
    appointment_time = serializers.TimeField()
    status = serializers.ChoiceField(
        choices=[
            "SCHEDULED",
            "CONFIRMED",
            "IN_PROGRESS",
            "COMPLETED",
            "CANCELLED",
            "NO_SHOW",
        ],
        required=False,
        default="SCHEDULED",
    )
    reason_for_visit = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)
