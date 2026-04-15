from rest_framework import serializers
from apps.documents.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    consultation = serializers.UUIDField(source="consultation.uuid", read_only=True)
    consultation_number = serializers.CharField(
        source="consultation.consultation_number", read_only=True
    )
    document_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = (
            "uuid",
            "document_type",
            "consultation",
            "consultation_number",
            "document",
            "document_url",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )

    def get_document_url(self, obj):
        request = self.context.get("request")
        if obj.document:
            if request:
                return request.build_absolute_uri(obj.document.url)
            return obj.document.url
        return None


class DocumentCreateSerializer(serializers.Serializer):
    document_type = serializers.CharField(max_length=255)
    consultation_id = serializers.UUIDField()
    document = serializers.FileField()
    description = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)


class DocumentUpdateSerializer(serializers.Serializer):
    document_type = serializers.CharField(max_length=255, required=False)
    consultation_id = serializers.UUIDField(required=False)
    document = serializers.FileField(required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
