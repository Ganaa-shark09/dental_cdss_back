from datetime import date

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.patients.models import Patient


class PatientService:
    PATIENT_CODE_PREFIX = "PAT"
    PATIENT_CODE_PADDING = 5

    @staticmethod
    def validate_email_uniqueness(email: str):
        if email and Patient.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                {"email": ["A patient with this email already exists."]}
            )

    @staticmethod
    def validate_email_uniqueness_for_update(email: str, patient_uuid):
        if (
            email
            and Patient.objects.filter(email__iexact=email)
            .exclude(uuid=patient_uuid)
            .exists()
        ):
            raise ValidationError(
                {"email": ["A patient with this email already exists."]}
            )

    @staticmethod
    def validate_date_of_birth(date_of_birth):
        if date_of_birth and date_of_birth > date.today():
            raise ValidationError(
                {"date_of_birth": ["Date of birth cannot be in the future."]}
            )

    @classmethod
    def build_patient_code(cls, patient_id: int) -> str:
        return f"{cls.PATIENT_CODE_PREFIX}{str(patient_id).zfill(cls.PATIENT_CODE_PADDING)}"

    @classmethod
    @transaction.atomic
    def create_patient(cls, validated_data):
        email = validated_data.get("email")
        email = email.strip().lower() if email else None

        cls.validate_email_uniqueness(email)
        cls.validate_date_of_birth(validated_data.get("date_of_birth"))

        patient = Patient.objects.create(
            patient_code="TEMP",
            first_name=validated_data["first_name"].strip(),
            last_name=validated_data.get("last_name", "").strip() or None,
            gender=validated_data["gender"],
            date_of_birth=validated_data.get("date_of_birth"),
            phone_number=validated_data.get("phone_number", "").strip() or None,
            email=email,
            address=validated_data.get("address", "").strip() or None,
            city=validated_data.get("city", "").strip() or None,
            state=validated_data.get("state", "").strip() or None,
            country=validated_data.get("country", "").strip() or None,
            postal_code=validated_data.get("postal_code", "").strip() or None,
            blood_group=validated_data.get("blood_group", "").strip() or None,
            marital_status=validated_data.get("marital_status", "").strip() or None,
            occupation=validated_data.get("occupation", "").strip() or None,
            emergency_contact_name=validated_data.get(
                "emergency_contact_name", ""
            ).strip()
            or None,
            emergency_contact_phone=validated_data.get(
                "emergency_contact_phone", ""
            ).strip()
            or None,
            is_active=validated_data.get("is_active", True),
        )

        patient.patient_code = cls.build_patient_code(patient.id)
        patient.save(update_fields=["patient_code"])

        return patient

    @staticmethod
    def list_patients():
        return Patient.objects.all().order_by("-created_at")

    @staticmethod
    def get_patient_by_uuid(patient_uuid):
        try:
            return Patient.objects.get(uuid=patient_uuid)
        except Patient.DoesNotExist:
            raise ValidationError({"patient_uuid": ["Patient not found."]})

    @classmethod
    def update_patient(cls, patient_uuid, validated_data):
        patient = cls.get_patient_by_uuid(patient_uuid)

        email = validated_data.get("email")
        email = email.strip().lower() if email else None

        cls.validate_email_uniqueness_for_update(email, patient_uuid)
        cls.validate_date_of_birth(validated_data.get("date_of_birth"))

        patient.first_name = validated_data["first_name"].strip()
        patient.last_name = validated_data.get("last_name", "").strip() or None
        patient.gender = validated_data["gender"]
        patient.date_of_birth = validated_data.get("date_of_birth")
        patient.phone_number = validated_data.get("phone_number", "").strip() or None
        patient.email = email
        patient.address = validated_data.get("address", "").strip() or None
        patient.city = validated_data.get("city", "").strip() or None
        patient.state = validated_data.get("state", "").strip() or None
        patient.country = validated_data.get("country", "").strip() or None
        patient.postal_code = validated_data.get("postal_code", "").strip() or None
        patient.blood_group = validated_data.get("blood_group", "").strip() or None
        patient.marital_status = (
            validated_data.get("marital_status", "").strip() or None
        )
        patient.occupation = validated_data.get("occupation", "").strip() or None
        patient.emergency_contact_name = (
            validated_data.get("emergency_contact_name", "").strip() or None
        )
        patient.emergency_contact_phone = (
            validated_data.get("emergency_contact_phone", "").strip() or None
        )
        patient.is_active = validated_data.get("is_active", patient.is_active)

        patient.save()
        return patient
