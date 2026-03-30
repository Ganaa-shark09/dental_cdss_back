from rest_framework import serializers
from apps.prescriptions.models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = (
            "id",
            "consultation",
            "patient",
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
