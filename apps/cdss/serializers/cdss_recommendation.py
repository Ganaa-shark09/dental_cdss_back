from rest_framework import serializers
from apps.cdss.models import CdssRecommendation


class CdssRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CdssRecommendation
        fields = (
            "uuid",
            "cdss_engine",
            "recommendation",
            "is_active",
            "created_at",
            "updated_at",
        )
