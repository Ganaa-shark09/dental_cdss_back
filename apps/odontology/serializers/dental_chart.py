from rest_framework import serializers

from apps.odontology.models import DentalChart
from apps.odontology.serializers.tooth_record import ToothRecordSerializer


class DentalChartSerializer(serializers.ModelSerializer):
    consultation_number = serializers.CharField(
        source="consultation.consultation_number",
        read_only=True,
    )
    tooth_records = ToothRecordSerializer(many=True, read_only=True)

    class Meta:
        model = DentalChart
        fields = (
            "id",
            "consultation",
            "consultation_number",
            "notes",
            "is_active",
            "tooth_records",
            "created_at",
            "updated_at",
        )


class DentalChartCreateSerializer(serializers.Serializer):
    consultation_id = serializers.UUIDField()
    notes = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)
