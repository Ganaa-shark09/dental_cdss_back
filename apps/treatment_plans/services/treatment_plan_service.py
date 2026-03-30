from rest_framework.exceptions import ValidationError
from apps.treatment_plans.models import TreatmentPlan
from apps.consultations.models import Consultation


class TreatmentPlanService:
    @staticmethod
    def get_consultation(consultation_id):
        try:
            return Consultation.objects.get(id=consultation_id, is_active=True)
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid consultation not found."]}
            )

    @classmethod
    def create_treatment_plan(cls, validated_data):
        consultation = cls.get_consultation(validated_data["consultation_id"])

        treatment_plan = TreatmentPlan.objects.create(
            consultation=consultation,
            treatment_type=validated_data["treatment_type"].strip(),
            treatment_description=validated_data["treatment_description"].strip(),
            start_date=validated_data.get("start_date"),
            end_date=validated_data.get("end_date"),
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
    def get_treatment_plan_by_id(treatment_plan_id):
        try:
            return TreatmentPlan.objects.select_related("consultation").get(
                id=treatment_plan_id
            )
        except TreatmentPlan.DoesNotExist:
            raise ValidationError({"treatment_plan_id": ["Treatment plan not found."]})
