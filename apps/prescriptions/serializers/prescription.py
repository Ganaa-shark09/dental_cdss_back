from rest_framework import serializers
from apps.prescriptions.models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    consultation = serializers.UUIDField(source="consultation.uuid", read_only=True)
    consultation_number = serializers.CharField(
        source="consultation.consultation_number", read_only=True
    )
    patient = serializers.UUIDField(source="patient.uuid", read_only=True)
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)

    class Meta:
        model = Prescription
        fields = (
            "uuid",
            "consultation",
            "consultation_number",
            "patient",
            "patient_name",
            "medication",
            "dosage",
            "treatment_instructions",
            "notes",
            "date_issued",
            "expiry_date",
            "is_active",
            "created_at",
            "updated_at",
        )


class PrescriptionCreateSerializer(serializers.Serializer):
    consultation_id = serializers.UUIDField()
    patient_id = serializers.UUIDField()
    medication = serializers.CharField(max_length=255)
    dosage = serializers.CharField(max_length=255)
    treatment_instructions = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)
    date_issued = serializers.DateField()
    expiry_date = serializers.DateField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False, default=True)


class PrescriptionUpdateSerializer(serializers.Serializer):
    consultation_id = serializers.UUIDField(required=False)
    patient_id = serializers.UUIDField(required=False)
    medication = serializers.CharField(max_length=255, required=False)
    dosage = serializers.CharField(max_length=255, required=False)
    treatment_instructions = serializers.CharField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    date_issued = serializers.DateField(required=False)
    expiry_date = serializers.DateField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)
