from rest_framework.exceptions import ValidationError
from apps.reports.models import Report
from apps.consultations.models import Consultation
from apps.prescriptions.models import Prescription
from apps.treatment_plans.models import TreatmentPlan
from apps.documents.models import Document


class ReportService:
    @staticmethod
    def get_consultation(consultation_id):
        try:
            return Consultation.objects.get(id=consultation_id, is_active=True)
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid consultation not found."]}
            )

    @staticmethod
    def get_prescription(prescription_id):
        if not prescription_id:
            return None
        try:
            return Prescription.objects.get(id=prescription_id)
        except Prescription.DoesNotExist:
            raise ValidationError(
                {"prescription_id": ["Valid prescription not found."]}
            )

    @staticmethod
    def get_treatment_plan(treatment_plan_id):
        if not treatment_plan_id:
            return None
        try:
            return TreatmentPlan.objects.get(id=treatment_plan_id)
        except TreatmentPlan.DoesNotExist:
            raise ValidationError(
                {"treatment_plan_id": ["Valid treatment plan not found."]}
            )

    @staticmethod
    def get_documents(document_ids):
        if not document_ids:
            return []
        return Document.objects.filter(id__in=document_ids)

    @classmethod
    def create_report(cls, validated_data):
        consultation = cls.get_consultation(validated_data["consultation_id"])
        prescription_summary = cls.get_prescription(
            validated_data.get("prescription_summary_id")
        )
        treatment_plan_summary = cls.get_treatment_plan(
            validated_data.get("treatment_plan_summary_id")
        )
        documents = cls.get_documents(validated_data.get("document_ids", []))

        report = Report.objects.create(
            consultation=consultation,
            report_type=validated_data["report_type"],
            prescription_summary=prescription_summary,
            treatment_plan_summary=treatment_plan_summary,
            notes=validated_data.get("notes", "").strip() or None,
            is_active=validated_data.get("is_active", True),
        )

        report.documents.set(documents)
        return report

    @staticmethod
    def list_reports():
        return (
            Report.objects.select_related("consultation").all().order_by("-created_at")
        )

    @staticmethod
    def get_report_by_id(report_id):
        try:
            return (
                Report.objects.select_related("consultation")
                .prefetch_related("documents")
                .get(id=report_id)
            )
        except Report.DoesNotExist:
            raise ValidationError({"report_id": ["Report not found."]})
