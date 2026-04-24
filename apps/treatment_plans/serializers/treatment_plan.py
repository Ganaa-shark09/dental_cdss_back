from rest_framework import serializers
from apps.treatment_plans.models import TreatmentPlan


class TreatmentPlanSerializer(serializers.ModelSerializer):
    consultation = serializers.UUIDField(source="consultation.uuid", read_only=True)
    consultation_number = serializers.CharField(
        source="consultation.consultation_number", read_only=True
    )

    class Meta:
        model = TreatmentPlan
        fields = (
            "uuid",
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
        choices=["PLANNED", "IN_PROGRESS", "COMPLETED"],
        required=False,
        default="PLANNED",
    )
    is_active = serializers.BooleanField(required=False, default=True)


class TreatmentPlanUpdateSerializer(serializers.Serializer):
    consultation_id = serializers.UUIDField(required=False)
    treatment_type = serializers.CharField(max_length=255, required=False)
    treatment_description = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=["PLANNED", "IN_PROGRESS", "COMPLETED"],
        required=False,
    )
    is_active = serializers.BooleanField(required=False)
