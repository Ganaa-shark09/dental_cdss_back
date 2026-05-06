from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.audit_logs.services import AuditLogService
from apps.documents.models import Document
from apps.consultations.models import Consultation


class DocumentService:
    @staticmethod
    def get_consultation(consultation_uuid):
        try:
            return Consultation.objects.get(uuid=consultation_uuid, is_active=True)
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid consultation not found."]}
            )

    @staticmethod
    def get_document_by_uuid(document_uuid):
        try:
            return Document.objects.select_related("consultation").get(
                uuid=document_uuid
            )
        except Document.DoesNotExist:
            raise ValidationError({"document_uuid": ["Document not found."]})

    @classmethod
    @transaction.atomic
    def create_document(cls, validated_data, user):
        consultation = cls.get_consultation(validated_data["consultation_id"])

        document = Document.objects.create(
            consultation=consultation,
            document_type=validated_data["document_type"].strip(),
            document=validated_data["document"],
            description=validated_data.get("description", "").strip() or None,
            is_active=validated_data.get("is_active", True),
        )

        AuditLogService.create_log(
            model_name="Document",
            record_id=document.uuid,
            field_name="created",
            old_value=None,
            new_value=f"{document.document_type} - Consultation {consultation.uuid}",
            user=user,
        )

        return document

    @classmethod
    @transaction.atomic
    def update_document(cls, document_uuid, validated_data, user):
        document_obj = cls.get_document_by_uuid(document_uuid)

        # Capture old values before modifications
        old_values = {
            "consultation": str(document_obj.consultation.uuid),
            "document_type": document_obj.document_type,
            "description": document_obj.description,
            "is_active": document_obj.is_active,
        }

        if "consultation_id" in validated_data:
            document_obj.consultation = cls.get_consultation(
                validated_data["consultation_id"]
            )

        if "document_type" in validated_data:
            document_obj.document_type = validated_data["document_type"].strip()

        if "document" in validated_data:
            document_obj.document = validated_data["document"]

        if "description" in validated_data:
            document_obj.description = (
                validated_data.get("description", "").strip() or None
            )

        if "is_active" in validated_data:
            document_obj.is_active = validated_data["is_active"]

        document_obj.save()

        # Log each changed field
        new_values = {
            "consultation": str(document_obj.consultation.uuid),
            "document_type": document_obj.document_type,
            "description": document_obj.description,
            "is_active": document_obj.is_active,
        }

        for field_name, old_val in old_values.items():
            new_val = new_values[field_name]
            if str(old_val) != str(new_val):
                AuditLogService.create_log(
                    model_name="Document",
                    record_id=document_obj.uuid,
                    field_name=field_name,
                    old_value=old_val,
                    new_value=new_val,
                    user=user,
                )

        return document_obj

    @staticmethod
    def list_documents():
        return (
            Document.objects.select_related("consultation")
            .all()
            .order_by("-created_at")
        )
