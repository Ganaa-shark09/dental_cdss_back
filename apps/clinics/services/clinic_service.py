from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.audit_logs.services import AuditLogService
from apps.clinics.models import Clinic


class ClinicService:
    @staticmethod
    def validate_code_uniqueness(code: str):
        if Clinic.objects.filter(code__iexact=code).exists():
            raise ValidationError({"code": ["A clinic with this code already exists."]})

    @classmethod
    @transaction.atomic
    def create_clinic(cls, validated_data, user):
        code = validated_data["code"].strip().upper()
        cls.validate_code_uniqueness(code)

        clinic = Clinic.objects.create(
            name=validated_data["name"].strip(),
            code=code,
            email=validated_data.get("email") or None,
            phone_number=validated_data.get("phone_number", ""),
            address=validated_data.get("address", ""),
            city=validated_data.get("city", ""),
            state=validated_data.get("state", ""),
            country=validated_data.get("country", ""),
            postal_code=validated_data.get("postal_code", ""),
            is_active=validated_data.get("is_active", True),
        )

        AuditLogService.create_log(
            model_name="Clinic",
            record_id=clinic.uuid,
            field_name="created",
            old_value=None,
            new_value=clinic.code,
            user=user,
        )

        return clinic

    @staticmethod
    def list_clinics():
        return Clinic.objects.all().order_by("name")
