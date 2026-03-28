from rest_framework.exceptions import ValidationError

from apps.staff.models import StaffProfile
from apps.users.models import User
from apps.clinics.models import Clinic


class StaffService:
    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            raise ValidationError({"user_id": ["Valid active user not found."]})

    @staticmethod
    def get_clinic(clinic_id):
        try:
            return Clinic.objects.get(id=clinic_id, is_active=True)
        except Clinic.DoesNotExist:
            raise ValidationError({"clinic_id": ["Valid active clinic not found."]})

    @staticmethod
    def validate_employee_id(employee_id: str):
        if StaffProfile.objects.filter(employee_id__iexact=employee_id).exists():
            raise ValidationError(
                {
                    "employee_id": [
                        "A staff profile with this employee ID already exists."
                    ]
                }
            )

    @staticmethod
    def validate_user_not_already_assigned(user):
        if StaffProfile.objects.filter(user=user).exists():
            raise ValidationError(
                {"user_id": ["This user already has a staff profile."]}
            )

    @classmethod
    def create_staff_profile(cls, validated_data):
        user = validated_data["user"]
        clinic = validated_data["clinic"]
        employee_id = validated_data["employee_id"].strip().upper()

        cls.validate_employee_id(employee_id)
        cls.validate_user_not_already_assigned(user)

        staff_profile = StaffProfile.objects.create(
            user=user,
            clinic=clinic,
            employee_id=employee_id,
            designation=validated_data["designation"].strip(),
            specialization=validated_data.get("specialization", ""),
            license_number=validated_data.get("license_number", ""),
            years_of_experience=validated_data.get("years_of_experience", 0),
            is_active=validated_data.get("is_active", True),
        )
        return staff_profile

    @staticmethod
    def list_staff_profiles():
        return (
            StaffProfile.objects.select_related("user", "clinic")
            .all()
            .order_by("-created_at")
        )
