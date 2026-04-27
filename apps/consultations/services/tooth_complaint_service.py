from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError

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
    def create_tooth_complaint(consultation_id, validated_data):
        consultation = ToothComplaintService._get_consultation(consultation_id)
        tooth_number = validated_data["tooth_number"]

        if consultation.tooth_complaints.filter(tooth_number=tooth_number).exists():
            raise ValidationError(
                {"tooth_number": f"A complaint for tooth {tooth_number} already exists. Use PATCH to update."}
            )

        return ToothComplaint.objects.create(
            consultation=consultation,
            tooth_number=tooth_number,
            complaint_codes=validated_data.get("complaint_codes", []),
            duration=validated_data.get("duration", ""),
            severity=validated_data.get("severity", ""),
        )

    @staticmethod
    @transaction.atomic
    def bulk_create_or_update_tooth_complaints(consultation_id, teeth_data):
        """
        Upsert multiple tooth complaints in one call.
        Used by wizard when the frontend submits all teeth at once.
        """
        consultation = ToothComplaintService._get_consultation(consultation_id)
        results = []

        for item in teeth_data:
            tooth_number = item["tooth_number"]
            tc, _created = ToothComplaint.objects.update_or_create(
                consultation=consultation,
                tooth_number=tooth_number,
                defaults={
                    "complaint_codes": item.get("complaint_codes", []),
                    "duration": item.get("duration", "") or "",
                    "severity": item.get("severity", "") or "",
                },
            )
            results.append(tc)

        return results

    @staticmethod
    @transaction.atomic
    def update_tooth_complaint(consultation_id, tooth_complaint_id, validated_data):
        tc = ToothComplaintService.get_tooth_complaint(consultation_id, tooth_complaint_id)

        if "complaint_codes" in validated_data:
            tc.complaint_codes = validated_data["complaint_codes"]
        if "duration" in validated_data:
            tc.duration = validated_data["duration"]
        if "severity" in validated_data:
            tc.severity = validated_data["severity"]

        tc.save()
        return tc

    @staticmethod
    @transaction.atomic
    def delete_tooth_complaint(consultation_id, tooth_complaint_id):
        tc = ToothComplaintService.get_tooth_complaint(consultation_id, tooth_complaint_id)
        tc.delete()
