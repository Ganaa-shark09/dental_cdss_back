from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError

from apps.audit_logs.services import AuditLogService
from apps.consultations.models import Consultation, ToothComplaint


class ToothComplaintService:

    @staticmethod
    def _get_consultation(consultation_id):
        try:
            return Consultation.objects.get(uuid=consultation_id, is_active=True)
        except Consultation.DoesNotExist:
            raise NotFound(f"Consultation {consultation_id} not found.")

    @staticmethod
    def list_tooth_complaints(consultation_id):
        consultation = ToothComplaintService._get_consultation(consultation_id)
        return consultation.tooth_complaints.all().order_by("tooth_number")

    @staticmethod
    def get_tooth_complaint(consultation_id, tooth_complaint_id):
        consultation = ToothComplaintService._get_consultation(consultation_id)
        try:
            return consultation.tooth_complaints.get(uuid=tooth_complaint_id)
        except ToothComplaint.DoesNotExist:
            raise NotFound(f"ToothComplaint {tooth_complaint_id} not found.")

    @staticmethod
    @transaction.atomic
    def create_tooth_complaint(consultation_id, validated_data, user):
        consultation = ToothComplaintService._get_consultation(consultation_id)
        tooth_number = validated_data["tooth_number"]

        if consultation.tooth_complaints.filter(tooth_number=tooth_number).exists():
            raise ValidationError(
                {"tooth_number": f"A complaint for tooth {tooth_number} already exists. Use PATCH to update."}
            )

        tc = ToothComplaint.objects.create(
            consultation=consultation,
            tooth_number=tooth_number,
            complaint_codes=validated_data.get("complaint_codes", []),
            duration=validated_data.get("duration", ""),
            severity=validated_data.get("severity", ""),
        )

        AuditLogService.create_log(
            model_name="ToothComplaint",
            record_id=tc.uuid,
            field_name="created",
            old_value=None,
            new_value=f"Tooth {tooth_number} - Consultation {consultation_id}",
            user=user,
        )

        return tc

    @staticmethod
    @transaction.atomic
    def bulk_create_or_update_tooth_complaints(consultation_id, teeth_data, user):
        """
        Upsert multiple tooth complaints in one call.
        Used by wizard when the frontend submits all teeth at once.
        """
        consultation = ToothComplaintService._get_consultation(consultation_id)
        results = []

        for item in teeth_data:
            tooth_number = item["tooth_number"]
            existing = ToothComplaint.objects.filter(
                consultation=consultation,
                tooth_number=tooth_number,
            ).first()

            old_value = str(existing.complaint_codes) if existing else None
            is_created = existing is None

            tc, _created = ToothComplaint.objects.update_or_create(
                consultation=consultation,
                tooth_number=tooth_number,
                defaults={
                    "complaint_codes": item.get("complaint_codes", []),
                    "duration": item.get("duration", "") or "",
                    "severity": item.get("severity", "") or "",
                },
            )

            if is_created:
                AuditLogService.create_log(
                    model_name="ToothComplaint",
                    record_id=tc.uuid,
                    field_name="created",
                    old_value=None,
                    new_value=f"Tooth {tooth_number} - Consultation {consultation_id}",
                    user=user,
                )
            else:
                new_value = str(tc.complaint_codes)
                if old_value != new_value:
                    AuditLogService.create_log(
                        model_name="ToothComplaint",
                        record_id=tc.uuid,
                        field_name="complaint_codes",
                        old_value=old_value,
                        new_value=new_value,
                        user=user,
                    )

            results.append(tc)

        return results

    @staticmethod
    @transaction.atomic
    def update_tooth_complaint(consultation_id, tooth_complaint_id, validated_data, user):
        tc = ToothComplaintService.get_tooth_complaint(consultation_id, tooth_complaint_id)

        old_values = {
            "complaint_codes": str(tc.complaint_codes),
            "duration": tc.duration,
            "severity": tc.severity,
        }

        if "complaint_codes" in validated_data:
            tc.complaint_codes = validated_data["complaint_codes"]
        if "duration" in validated_data:
            tc.duration = validated_data["duration"]
        if "severity" in validated_data:
            tc.severity = validated_data["severity"]

        tc.save()

        new_values = {
            "complaint_codes": str(tc.complaint_codes),
            "duration": tc.duration,
            "severity": tc.severity,
        }

        for field_name, old_val in old_values.items():
            new_val = new_values[field_name]
            if str(old_val) != str(new_val):
                AuditLogService.create_log(
                    model_name="ToothComplaint",
                    record_id=tc.uuid,
                    field_name=field_name,
                    old_value=old_val,
                    new_value=new_val,
                    user=user,
                )

        return tc

    @staticmethod
    @transaction.atomic
    def delete_tooth_complaint(consultation_id, tooth_complaint_id, user):
        tc = ToothComplaintService.get_tooth_complaint(consultation_id, tooth_complaint_id)
        AuditLogService.create_log(
            model_name="ToothComplaint",
            record_id=tc.uuid,
            field_name="deleted",
            old_value=f"Tooth {tc.tooth_number} - Consultation {consultation_id}",
            new_value=None,
            user=user,
        )
        tc.delete()
