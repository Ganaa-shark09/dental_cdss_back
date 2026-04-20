from rest_framework import serializers
from apps.reports.models import Report
from apps.documents.models import Document


class ReportSerializer(serializers.ModelSerializer):
    consultation = serializers.UUIDField(source="consultation.uuid", read_only=True)
    consultation_number = serializers.CharField(
        source="consultation.consultation_number", read_only=True
    )

    prescription_summary = serializers.SerializerMethodField()
    treatment_plan_summary = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            "uuid",
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

    def get_prescription_summary(self, obj):
        if not obj.prescription_summary:
            return None
        return {
            "uuid": str(obj.prescription_summary.uuid),
            "medication": obj.prescription_summary.medication,
            "dosage": obj.prescription_summary.dosage,
        }

    def get_treatment_plan_summary(self, obj):
        if not obj.treatment_plan_summary:
            return None
        return {
            "uuid": str(obj.treatment_plan_summary.uuid),
            "treatment_type": obj.treatment_plan_summary.treatment_type,
            "status": obj.treatment_plan_summary.status,
        }

    def get_documents(self, obj):
        return [
            {
                "uuid": str(document.uuid),
                "document_type": document.document_type,
                "document": document.document.url if document.document else None,
                "description": document.description,
            }
            for document in obj.documents.all()
        ]


class ReportCreateSerializer(serializers.Serializer):
    consultation_id = serializers.UUIDField()
    report_type = serializers.CharField(max_length=255)
    prescription_summary_id = serializers.UUIDField(required=False, allow_null=True)
    treatment_plan_summary_id = serializers.UUIDField(required=False, allow_null=True)
    document_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        allow_empty=True,
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)


class ReportUpdateSerializer(serializers.Serializer):
    consultation_id = serializers.UUIDField(required=False)
    report_type = serializers.CharField(max_length=255, required=False)
    prescription_summary_id = serializers.UUIDField(required=False, allow_null=True)
    treatment_plan_summary_id = serializers.UUIDField(required=False, allow_null=True)
    document_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        allow_empty=True,
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
