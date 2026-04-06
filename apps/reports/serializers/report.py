from rest_framework import serializers
from apps.documents.models import Document
from apps.reports.models import Report


class ReportSerializer(serializers.ModelSerializer):
    consultation_number = serializers.CharField(
        source="consultation.consultation_number", read_only=True
    )
    prescription_summary = serializers.CharField(
        source="prescription_summary.medication", read_only=True, required=False
    )
    treatment_plan_summary = serializers.CharField(
        source="treatment_plan_summary.treatment_type", read_only=True, required=False
    )
    documents = serializers.SlugRelatedField(
        queryset=Document.objects.all(), slug_field="document_type", many=True
    )

    class Meta:
        model = Report
        fields = (
            "id",
            "consultation",
            "consultation_number",
            "report_type",
            "prescription_summary",
            "treatment_plan_summary",
            "documents",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
        )


from rest_framework import serializers


class ReportCreateSerializer(serializers.Serializer):
    consultation_id = serializers.UUIDField()
    report_type = serializers.CharField(max_length=255)
    prescription_summary_id = serializers.UUIDField(required=False, allow_null=True)
    treatment_plan_summary_id = serializers.UUIDField(required=False, allow_null=True)
    document_ids = serializers.ListField(
        child=serializers.UUIDField(), required=False, allow_empty=True
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)
