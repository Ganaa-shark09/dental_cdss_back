from rest_framework import serializers
from apps.cdss.models import CdssRecommendation


class CdssRecommendationSerializer(serializers.ModelSerializer):
    cdss_engine = serializers.UUIDField(source="cdss_engine.uuid", read_only=True)
    consultation = serializers.UUIDField(
        source="cdss_engine.consultation.uuid", read_only=True
    )
    consultation_number = serializers.CharField(
        source="cdss_engine.consultation.consultation_number", read_only=True
    )

    class Meta:
        model = CdssRecommendation
        fields = (
            "uuid",
            "cdss_engine",
            "consultation",
            "consultation_number",
            "recommendation",
            "is_active",
            "created_at",
            "updated_at",
        )
