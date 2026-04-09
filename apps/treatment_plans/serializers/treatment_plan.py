from rest_framework import serializers
from apps.treatment_plans.models import TreatmentPlan


class TreatmentPlanSerializer(serializers.ModelSerializer):
    consultation_number = serializers.CharField(
        source="consultation.consultation_number", read_only=True
    )

    class Meta:
        model = TreatmentPlan
        fields = (
            "id",
            "consultation",
            "consultation_number",
            "treatment_type",
            "treatment_description",
            "start_date",
            "end_date",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )


class TreatmentPlanCreateSerializer(serializers.Serializer):
    consultation_id = serializers.UUIDField()
    treatment_type = serializers.CharField(max_length=255)
    treatment_description = serializers.CharField()
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=["PLANNED", "IN_PROGRESS", "COMPLETED"], default="PLANNED"
    )
    is_active = serializers.BooleanField(required=False, default=True)
