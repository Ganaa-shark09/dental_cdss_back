from datetime import date

from rest_framework.exceptions import ValidationError

from apps.patients.models import Patient


class PatientService:
    @staticmethod
    def validate_patient_code_uniqueness(patient_code: str):
        if Patient.objects.filter(patient_code__iexact=patient_code).exists():
            raise ValidationError(
                {"patient_code": ["A patient with this patient code already exists."]}
            )

    @staticmethod
    def validate_email_uniqueness(email: str):
        if email and Patient.objects.filter(email__iexact=email).exists():
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
    def create_patient(cls, validated_data):
        patient_code = validated_data["patient_code"].strip().upper()
        email = validated_data.get("email")
        email = email.strip().lower() if email else None

        cls.validate_patient_code_uniqueness(patient_code)
        cls.validate_email_uniqueness(email)
        cls.validate_date_of_birth(validated_data.get("date_of_birth"))

        patient = Patient.objects.create(
            patient_code=patient_code,
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
        return patient

    @staticmethod
    def list_patients():
        return Patient.objects.all().order_by("-created_at")

    @staticmethod
    def get_patient_by_id(patient_id):
        try:
            return Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise ValidationError({"patient_id": ["Patient not found."]})
