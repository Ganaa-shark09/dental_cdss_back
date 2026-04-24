from rest_framework.exceptions import ValidationError

from apps.reports.models import Report
from apps.consultations.models import Consultation
from apps.prescriptions.models import Prescription
from apps.treatment_plans.models import TreatmentPlan
from apps.documents.models import Document


class ReportService:
    @staticmethod
    def get_consultation(consultation_uuid):
        try:
            return Consultation.objects.get(uuid=consultation_uuid, is_active=True)
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid consultation not found."]}
            )

    @staticmethod
    def get_prescription(prescription_uuid):
        if not prescription_uuid:
            return None
        try:
            return Prescription.objects.get(uuid=prescription_uuid, is_active=True)
        except Prescription.DoesNotExist:
            raise ValidationError(
                {"prescription_summary_id": ["Valid prescription not found."]}
            )

    @staticmethod
    def get_treatment_plan(treatment_plan_uuid):
        if not treatment_plan_uuid:
            return None
        try:
            return TreatmentPlan.objects.get(
                uuid=treatment_plan_uuid,
                is_active=True,
            )
        except TreatmentPlan.DoesNotExist:
            raise ValidationError(
                {"treatment_plan_summary_id": ["Valid treatment plan not found."]}
            )

    @staticmethod
    def get_documents(document_ids):
        if not document_ids:
            return []

        documents = list(Document.objects.filter(uuid__in=document_ids, is_active=True))
        found_ids = {str(document.uuid) for document in documents}
        requested_ids = {str(document_id) for document_id in document_ids}

        missing_ids = requested_ids - found_ids
        if missing_ids:
            raise ValidationError(
                {
                    "document_ids": [
                        f"Some documents were not found or inactive: {', '.join(sorted(missing_ids))}"
                    ]
                }
            )

        return documents

    @staticmethod
    def validate_related_records_belong_to_consultation(
        consultation,
        prescription_summary,
        treatment_plan_summary,
        documents,
    ):
        if (
            prescription_summary
            and prescription_summary.consultation_id != consultation.id
        ):
            raise ValidationError(
                {
                    "prescription_summary_id": [
                        "Selected prescription does not belong to the selected consultation."
                    ]
                }
            )

        if (
            treatment_plan_summary
            and treatment_plan_summary.consultation_id != consultation.id
        ):
            raise ValidationError(
                {
                    "treatment_plan_summary_id": [
                        "Selected treatment plan does not belong to the selected consultation."
                    ]
                }
            )

        invalid_documents = [
            str(document.uuid)
            for document in documents
            if document.consultation_id != consultation.id
        ]
        if invalid_documents:
            raise ValidationError(
                {
                    "document_ids": [
                        f"Some documents do not belong to the selected consultation: {', '.join(invalid_documents)}"
                    ]
                }
            )

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

        cls.validate_related_records_belong_to_consultation(
            consultation,
            prescription_summary,
            treatment_plan_summary,
            documents,
        )

        report = Report.objects.create(
            consultation=consultation,
            report_type=validated_data["report_type"].strip(),
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
            Report.objects.select_related(
                "consultation",
                "prescription_summary",
                "treatment_plan_summary",
            )
            .prefetch_related("documents")
            .all()
            .order_by("-created_at")
        )

    @staticmethod
    def get_report_by_uuid(report_uuid):
        try:
            return (
                Report.objects.select_related(
                    "consultation",
                    "prescription_summary",
                    "treatment_plan_summary",
                )
                .prefetch_related("documents")
                .get(uuid=report_uuid)
            )
        except Report.DoesNotExist:
            raise ValidationError({"report_uuid": ["Report not found."]})

    @classmethod
    def update_report(cls, report_uuid, validated_data):
        report = cls.get_report_by_uuid(report_uuid)

        consultation = (
            cls.get_consultation(validated_data["consultation_id"])
            if "consultation_id" in validated_data
            else report.consultation
        )
        prescription_summary = (
            cls.get_prescription(validated_data.get("prescription_summary_id"))
            if "prescription_summary_id" in validated_data
            else report.prescription_summary
        )
        treatment_plan_summary = (
            cls.get_treatment_plan(validated_data.get("treatment_plan_summary_id"))
            if "treatment_plan_summary_id" in validated_data
            else report.treatment_plan_summary
        )
        documents = (
            cls.get_documents(validated_data.get("document_ids", []))
            if "document_ids" in validated_data
            else list(report.documents.all())
        )

        cls.validate_related_records_belong_to_consultation(
            consultation,
            prescription_summary,
            treatment_plan_summary,
            documents,
        )

        report.consultation = consultation
        report.prescription_summary = prescription_summary
        report.treatment_plan_summary = treatment_plan_summary

        if "report_type" in validated_data:
            report.report_type = validated_data["report_type"].strip()

        if "notes" in validated_data:
            report.notes = validated_data.get("notes", "").strip() or None

        if "is_active" in validated_data:
            report.is_active = validated_data["is_active"]

        report.save()

        if "document_ids" in validated_data:
            report.documents.set(documents)

        return report
