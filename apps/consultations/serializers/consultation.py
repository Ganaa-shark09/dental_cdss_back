from rest_framework import serializers

from apps.consultations.models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):
    appointment = serializers.SerializerMethodField()
    patient = serializers.UUIDField(source="patient.uuid", read_only=True)
    clinic = serializers.UUIDField(source="clinic.uuid", read_only=True)
    staff_profile = serializers.SerializerMethodField()

    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    clinic_name = serializers.CharField(source="clinic.name", read_only=True)
    staff_name = serializers.SerializerMethodField()
    appointment_number = serializers.CharField(
        source="appointment.appointment_number", read_only=True
    )

    class Meta:
        model = Consultation
        fields = (
            "uuid",
            "appointment",
            "appointment_number",
            "patient",
            "patient_name",
            "clinic",
            "clinic_name",
            "staff_profile",
            "staff_name",
            "consultation_number",
            "consultation_date",
            "consultation_time",
            "chief_complaint",
            "history_of_present_illness",
            "medical_history_summary",
            "dental_history_summary",
            "examination_summary",
            "provisional_diagnosis",
            "final_diagnosis",
            "notes",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )

    def get_appointment(self, obj):
        return str(obj.appointment.uuid) if obj.appointment else None

    def get_staff_profile(self, obj):
        return str(obj.staff_profile.uuid) if obj.staff_profile else None

    def get_staff_name(self, obj):
        return obj.staff_profile.user.full_name if obj.staff_profile else None


class ConsultationCreateSerializer(serializers.Serializer):
    appointment_id = serializers.UUIDField(required=False, allow_null=True)
    patient_id = serializers.UUIDField()
    clinic_id = serializers.UUIDField()
    staff_profile_id = serializers.UUIDField(required=False, allow_null=True)

    consultation_date = serializers.DateField()
    consultation_time = serializers.TimeField()

    chief_complaint = serializers.CharField(required=False, allow_blank=True)
    history_of_present_illness = serializers.CharField(required=False, allow_blank=True)
    medical_history_summary = serializers.CharField(required=False, allow_blank=True)
    dental_history_summary = serializers.CharField(required=False, allow_blank=True)
    examination_summary = serializers.CharField(required=False, allow_blank=True)

    provisional_diagnosis = serializers.CharField(required=False, allow_blank=True)
    final_diagnosis = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    status = serializers.ChoiceField(
        choices=["DRAFT", "IN_PROGRESS", "COMPLETED", "CANCELLED"],
        required=False,
        default="DRAFT",
    )
    is_active = serializers.BooleanField(required=False, default=True)


class ConsultationUpdateSerializer(serializers.Serializer):
    appointment_id = serializers.UUIDField(required=False, allow_null=True)
    patient_id = serializers.UUIDField(required=False)
    clinic_id = serializers.UUIDField(required=False)
    staff_profile_id = serializers.UUIDField(required=False, allow_null=True)

    consultation_date = serializers.DateField(required=False)
    consultation_time = serializers.TimeField(required=False)

    chief_complaint = serializers.CharField(required=False, allow_blank=True)
    history_of_present_illness = serializers.CharField(required=False, allow_blank=True)
    medical_history_summary = serializers.CharField(required=False, allow_blank=True)
    dental_history_summary = serializers.CharField(required=False, allow_blank=True)
    examination_summary = serializers.CharField(required=False, allow_blank=True)

    provisional_diagnosis = serializers.CharField(required=False, allow_blank=True)
    final_diagnosis = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    status = serializers.ChoiceField(
        choices=["DRAFT", "IN_PROGRESS", "COMPLETED", "CANCELLED"],
        required=False,
    )
    is_active = serializers.BooleanField(required=False)
