from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.audit_logs.services import AuditLogService
from apps.staff.models import StaffProfile


class StaffService:
    EMPLOYEE_ID_PREFIX = "EMP"
    EMPLOYEE_ID_PADDING = 5

    @staticmethod
    def validate_user_not_already_assigned(user):
        if StaffProfile.objects.filter(user=user).exists():
            raise ValidationError({"user": ["This user already has a staff profile."]})

    @staticmethod
    def validate_user_not_already_assigned_for_update(user, staff_uuid):
        if StaffProfile.objects.filter(user=user).exclude(uuid=staff_uuid).exists():
            raise ValidationError({"user": ["This user already has a staff profile."]})

    @classmethod
    def build_employee_id(cls, staff_id: int) -> str:
        return f"{cls.EMPLOYEE_ID_PREFIX}{str(staff_id).zfill(cls.EMPLOYEE_ID_PADDING)}"

    @classmethod
    @transaction.atomic
    def create_staff_profile(cls, validated_data, user):
        user_obj = validated_data["user"]
        clinic = validated_data["clinic"]

        cls.validate_user_not_already_assigned(user_obj)

        staff_profile = StaffProfile.objects.create(
            user=user_obj,
            clinic=clinic,
            employee_id="TEMP",
            designation=validated_data["designation"].strip(),
            specialization=validated_data.get("specialization", "").strip() or None,
            license_number=validated_data.get("license_number", "").strip() or None,
            years_of_experience=validated_data.get("years_of_experience", 0),
            is_active=validated_data.get("is_active", True),
        )

        staff_profile.employee_id = cls.build_employee_id(staff_profile.id)
        staff_profile.save(update_fields=["employee_id"])

        AuditLogService.create_log(
            model_name="StaffProfile",
            record_id=staff_profile.uuid,
            field_name="created",
            old_value=None,
            new_value=staff_profile.employee_id,
            user=user,
        )

        return staff_profile

    @staticmethod
    def list_staff_profiles():
        return (
            StaffProfile.objects.select_related("user", "clinic")
            .all()
            .order_by("-created_at")
        )

    @staticmethod
    def get_staff_profile_by_uuid(staff_uuid):
        try:
            return StaffProfile.objects.select_related("user", "clinic").get(
                uuid=staff_uuid
            )
        except StaffProfile.DoesNotExist:
            raise ValidationError({"staff_uuid": ["Staff profile not found."]})

    @classmethod
    @transaction.atomic
    def update_staff_profile(cls, staff_uuid, validated_data, user):
        staff_profile = cls.get_staff_profile_by_uuid(staff_uuid)

        # Capture old values before modifications
        old_values = {
            "clinic": str(staff_profile.clinic.uuid),
            "designation": staff_profile.designation,
            "specialization": staff_profile.specialization,
            "license_number": staff_profile.license_number,
            "years_of_experience": staff_profile.years_of_experience,
            "is_active": staff_profile.is_active,
        }

        if "clinic" in validated_data:
            staff_profile.clinic = validated_data["clinic"]

        if "designation" in validated_data:
            staff_profile.designation = validated_data["designation"].strip()

        if "specialization" in validated_data:
            staff_profile.specialization = (
                validated_data.get("specialization", "").strip() or None
            )

        if "license_number" in validated_data:
            staff_profile.license_number = (
                validated_data.get("license_number", "").strip() or None
            )

        if "years_of_experience" in validated_data:
            staff_profile.years_of_experience = validated_data["years_of_experience"]

        if "is_active" in validated_data:
            staff_profile.is_active = validated_data["is_active"]

        staff_profile.save()

        # Log each changed field
        new_values = {
            "clinic": str(staff_profile.clinic.uuid),
            "designation": staff_profile.designation,
            "specialization": staff_profile.specialization,
            "license_number": staff_profile.license_number,
            "years_of_experience": staff_profile.years_of_experience,
            "is_active": staff_profile.is_active,
        }

        for field_name, old_val in old_values.items():
            new_val = new_values[field_name]
            if str(old_val) != str(new_val):
                AuditLogService.create_log(
                    model_name="StaffProfile",
                    record_id=staff_profile.uuid,
                    field_name=field_name,
                    old_value=old_val,
                    new_value=new_val,
                    user=user,
                )

        return staff_profile
