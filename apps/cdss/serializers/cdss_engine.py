from rest_framework import serializers
from apps.cdss.models import CdssEngine


class CdssEngineSerializer(serializers.ModelSerializer):
    consultation = serializers.UUIDField(source="consultation.uuid", read_only=True)
    consultation_number = serializers.CharField(
        source="consultation.consultation_number", read_only=True
    )

    class Meta:
        model = CdssEngine
        fields = (
            "uuid",
            "consultation",
            "consultation_number",
            "risk_score",
            "alerts",
            "recommendations",
            "diagnosis_assistance",
            "is_active",
            "created_at",
            "updated_at",
        )


class CdssEngineUpdateSerializer(serializers.Serializer):
    risk_score = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False
    )
    alerts = serializers.ListField(child=serializers.CharField(), required=False)
    recommendations = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    diagnosis_assistance = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
