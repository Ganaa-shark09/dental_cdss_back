from rest_framework import serializers

from apps.odontology.models import ToothRecord


class ToothRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToothRecord
        fields = (
            "id",
            "chart",
            "tooth_number",
            "condition",
            "surfaces",
            "mobility_grade",
            "percussion_tenderness",
            "palpation_tenderness",
            "probing_depth_summary",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
        )


class ToothRecordCreateSerializer(serializers.Serializer):
    tooth_number = serializers.CharField(max_length=10)
    condition = serializers.ChoiceField(
        choices=[
            "SOUND",
            "CARIES",
            "FILLED",
            "MISSING",
            "FRACTURED",
            "MOBILE",
            "ROOT_STUMP",
            "IMPACTED",
            "ATTRITION",
            "ABRASION",
            "ABFRACTION",
            "DISCOLORED",
        ]
    )
    surfaces = serializers.ListField(
        child=serializers.CharField(max_length=20),
        required=False,
        default=list,
    )
    mobility_grade = serializers.CharField(
        max_length=20, required=False, allow_blank=True
    )
    percussion_tenderness = serializers.BooleanField(required=False, default=False)
    palpation_tenderness = serializers.BooleanField(required=False, default=False)
    probing_depth_summary = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)
