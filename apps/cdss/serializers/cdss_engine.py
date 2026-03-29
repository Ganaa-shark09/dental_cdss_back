from rest_framework import serializers
from apps.cdss.models import CdssEngine


class CdssEngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CdssEngine
        fields = (
            "id",
            "consultation",
            "risk_score",
            "alerts",
            "recommendations",
            "diagnosis_assistance",
            "is_active",
            "created_at",
            "updated_at",
        )
