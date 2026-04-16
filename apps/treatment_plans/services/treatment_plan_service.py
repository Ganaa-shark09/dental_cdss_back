from rest_framework.exceptions import ValidationError

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
    def create_treatment_plan(cls, validated_data):
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
    def update_treatment_plan(cls, treatment_plan_uuid, validated_data):
        treatment_plan = cls.get_treatment_plan_by_uuid(treatment_plan_uuid)

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
        return treatment_plan
