from rest_framework.exceptions import ValidationError

from apps.prescriptions.models import Prescription
from apps.consultations.models import Consultation
from apps.patients.models import Patient


class PrescriptionService:
    @staticmethod
    def get_consultation(consultation_uuid):
        try:
            return Consultation.objects.select_related("patient").get(
                uuid=consultation_uuid,
                is_active=True,
            )
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid consultation not found."]}
            )

    @staticmethod
    def get_patient(patient_uuid):
        try:
            return Patient.objects.get(uuid=patient_uuid, is_active=True)
        except Patient.DoesNotExist:
            raise ValidationError({"patient_id": ["Valid patient not found."]})

    @staticmethod
    def validate_consultation_patient_match(consultation, patient):
        if consultation.patient_id != patient.id:
            raise ValidationError(
                {
                    "patient_id": [
                        "Selected patient does not match the consultation patient."
                    ]
                }
            )

    @staticmethod
    def validate_expiry_date(date_issued, expiry_date):
        if expiry_date and expiry_date < date_issued:
            raise ValidationError(
                {"expiry_date": ["Expiry date cannot be earlier than date issued."]}
            )

    @classmethod
    def create_prescription(cls, validated_data):
        consultation = cls.get_consultation(validated_data["consultation_id"])
        patient = cls.get_patient(validated_data["patient_id"])

        cls.validate_consultation_patient_match(consultation, patient)
        cls.validate_expiry_date(
            validated_data["date_issued"],
            validated_data.get("expiry_date"),
        )

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
            .order_by("-date_issued", "-created_at")
        )

    @staticmethod
    def get_prescription_by_uuid(prescription_uuid):
        try:
            return Prescription.objects.select_related("consultation", "patient").get(
                uuid=prescription_uuid
            )
        except Prescription.DoesNotExist:
            raise ValidationError({"prescription_id": ["Prescription not found."]})

    @classmethod
    def update_prescription(cls, prescription_uuid, validated_data):
        prescription = cls.get_prescription_by_uuid(prescription_uuid)

        consultation = (
            cls.get_consultation(validated_data["consultation_id"])
            if "consultation_id" in validated_data
            else prescription.consultation
        )

        patient = (
            cls.get_patient(validated_data["patient_id"])
            if "patient_id" in validated_data
            else prescription.patient
        )

        cls.validate_consultation_patient_match(consultation, patient)

        date_issued = validated_data.get("date_issued", prescription.date_issued)
        expiry_date = (
            validated_data["expiry_date"]
            if "expiry_date" in validated_data
            else prescription.expiry_date
        )
        cls.validate_expiry_date(date_issued, expiry_date)

        prescription.consultation = consultation
        prescription.patient = patient

        if "medication" in validated_data:
            prescription.medication = validated_data["medication"].strip()

        if "dosage" in validated_data:
            prescription.dosage = validated_data["dosage"].strip()

        if "treatment_instructions" in validated_data:
            prescription.treatment_instructions = validated_data[
                "treatment_instructions"
            ].strip()

        if "notes" in validated_data:
            prescription.notes = validated_data.get("notes", "").strip() or None

        if "date_issued" in validated_data:
            prescription.date_issued = validated_data["date_issued"]

        if "expiry_date" in validated_data:
            prescription.expiry_date = validated_data.get("expiry_date")

        if "is_active" in validated_data:
            prescription.is_active = validated_data["is_active"]

        prescription.save()
        return prescription
