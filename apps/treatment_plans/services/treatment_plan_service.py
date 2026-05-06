from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.audit_logs.services import AuditLogService
from apps.treatment_plans.models import TreatmentPlan
from apps.consultations.models import Consultation


class TreatmentPlanService:
    @staticmethod
    def get_consultation(consultation_uuid):
        try:
            return Consultation.objects.get(uuid=consultation_uuid, is_active=True)
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid consultation not found."]}
            )

    @staticmethod
    def validate_dates(start_date, end_date):
        if start_date and end_date and end_date < start_date:
            raise ValidationError(
                {"end_date": ["End date cannot be earlier than start date."]}
            )

    @classmethod
    @transaction.atomic
    def create_treatment_plan(cls, validated_data, user):
        consultation = cls.get_consultation(validated_data["consultation_id"])

        start_date = validated_data.get("start_date")
        end_date = validated_data.get("end_date")
        cls.validate_dates(start_date, end_date)

        treatment_plan = TreatmentPlan.objects.create(
            consultation=consultation,
            treatment_type=validated_data["treatment_type"].strip(),
            treatment_description=validated_data["treatment_description"].strip(),
            start_date=start_date,
            end_date=end_date,
            status=validated_data.get("status", TreatmentPlan.STATUS_PLANNED),
            is_active=validated_data.get("is_active", True),
        )

        AuditLogService.create_log(
            model_name="TreatmentPlan",
            record_id=treatment_plan.uuid,
            field_name="created",
            old_value=None,
            new_value=f"{treatment_plan.treatment_type} - {treatment_plan.status}",
            user=user,
        )

        return treatment_plan

    @staticmethod
    def list_treatment_plans():
        return (
            TreatmentPlan.objects.select_related("consultation")
            .all()
            .order_by("-created_at")
        )

    @staticmethod
    def get_treatment_plan_by_uuid(treatment_plan_uuid):
        try:
            return TreatmentPlan.objects.select_related("consultation").get(
                uuid=treatment_plan_uuid
            )
        except TreatmentPlan.DoesNotExist:
            raise ValidationError(
                {"treatment_plan_uuid": ["Treatment plan not found."]}
            )

    @classmethod
    @transaction.atomic
    def update_treatment_plan(cls, treatment_plan_uuid, validated_data, user):
        treatment_plan = cls.get_treatment_plan_by_uuid(treatment_plan_uuid)

        # Capture old values before modifications
        old_values = {
            "consultation": str(treatment_plan.consultation.uuid),
            "treatment_type": treatment_plan.treatment_type,
            "treatment_description": treatment_plan.treatment_description,
            "start_date": str(treatment_plan.start_date),
            "end_date": str(treatment_plan.end_date),
            "status": treatment_plan.status,
            "is_active": treatment_plan.is_active,
        }

        consultation = (
            cls.get_consultation(validated_data["consultation_id"])
            if "consultation_id" in validated_data
            else treatment_plan.consultation
        )

        start_date = (
            validated_data["start_date"]
            if "start_date" in validated_data
            else treatment_plan.start_date
        )
        end_date = (
            validated_data["end_date"]
            if "end_date" in validated_data
            else treatment_plan.end_date
        )

        cls.validate_dates(start_date, end_date)

        treatment_plan.consultation = consultation

        if "treatment_type" in validated_data:
            treatment_plan.treatment_type = validated_data["treatment_type"].strip()

        if "treatment_description" in validated_data:
            treatment_plan.treatment_description = validated_data[
                "treatment_description"
            ].strip()

        treatment_plan.start_date = start_date
        treatment_plan.end_date = end_date

        if "status" in validated_data:
            treatment_plan.status = validated_data["status"]

        if "is_active" in validated_data:
            treatment_plan.is_active = validated_data["is_active"]

        treatment_plan.save()

        # Log each changed field
        new_values = {
            "consultation": str(treatment_plan.consultation.uuid),
            "treatment_type": treatment_plan.treatment_type,
            "treatment_description": treatment_plan.treatment_description,
            "start_date": str(treatment_plan.start_date),
            "end_date": str(treatment_plan.end_date),
            "status": treatment_plan.status,
            "is_active": treatment_plan.is_active,
        }

        for field_name, old_val in old_values.items():
            new_val = new_values[field_name]
            if str(old_val) != str(new_val):
                AuditLogService.create_log(
                    model_name="TreatmentPlan",
                    record_id=treatment_plan.uuid,
                    field_name=field_name,
                    old_value=old_val,
                    new_value=new_val,
                    user=user,
                )

        return treatment_plan
