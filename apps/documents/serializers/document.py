from rest_framework import serializers
from apps.documents.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            "id",
            "document_type",
            "consultation",
            "document",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )


class DocumentCreateSerializer(serializers.Serializer):
    document_type = serializers.CharField(max_length=255)
    consultation_id = serializers.UUIDField()
    document = serializers.FileField()
    description = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)
