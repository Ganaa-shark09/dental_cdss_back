from rest_framework.exceptions import ValidationError
from apps.documents.models import Document
from apps.consultations.models import Consultation


class DocumentService:
    @staticmethod
    def get_consultation(consultation_id):
        try:
            return Consultation.objects.get(id=consultation_id, is_active=True)
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid consultation not found."]}
            )

    @classmethod
    def create_document(cls, validated_data):
        consultation = cls.get_consultation(validated_data["consultation_id"])

        document = Document.objects.create(
            consultation=consultation,
            document_type=validated_data["document_type"],
            document=validated_data["document"],
            description=validated_data.get("description", "").strip() or None,
            is_active=validated_data.get("is_active", True),
        )
        return document

    @staticmethod
    def list_documents():
        return (
            Document.objects.select_related("consultation")
            .all()
            .order_by("-created_at")
        )
