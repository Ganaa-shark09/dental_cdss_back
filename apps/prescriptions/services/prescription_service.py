from rest_framework.exceptions import ValidationError
from apps.prescriptions.models import Prescription
from apps.consultations.models import Consultation
from apps.patients.models import Patient


class PrescriptionService:
    @staticmethod
    def get_consultation(consultation_id):
        try:
            return Consultation.objects.get(id=consultation_id, is_active=True)
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid consultation not found."]}
            )

    @staticmethod
    def get_patient(patient_id):
        try:
            return Patient.objects.get(id=patient_id, is_active=True)
        except Patient.DoesNotExist:
            raise ValidationError({"patient_id": ["Valid patient not found."]})

    @classmethod
    def create_prescription(cls, validated_data):
        consultation = cls.get_consultation(validated_data["consultation_id"])
        patient = cls.get_patient(validated_data["patient_id"])

        prescription = Prescription.objects.create(
            consultation=consultation,
            patient=patient,
            medication=validated_data["medication"].strip(),
            dosage=validated_data["dosage"].strip(),
            treatment_instructions=validated_data["treatment_instructions"].strip(),
            notes=validated_data.get("notes", "").strip() or None,
            date_issued=validated_data["date_issued"],
            expiry_date=validated_data.get("expiry_date"),
            is_active=validated_data.get("is_active", True),
        )
        return prescription

    @staticmethod
    def list_prescriptions():
        return (
            Prescription.objects.select_related("consultation", "patient")
            .all()
            .order_by("-date_issued")
        )
