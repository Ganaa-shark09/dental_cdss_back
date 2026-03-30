from django.db import models

from apps.common.models import BaseModel
from apps.consultations.models import Consultation
import uuid


class Document(BaseModel):

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    document_type = models.CharField(max_length=255)
    consultation = models.ForeignKey(
        "consultations.Consultation", on_delete=models.CASCADE, related_name="documents"
    )
    document = models.FileField(upload_to="documents/")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "documents"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Document for {self.consultation.consultation_number} - {self.document_type}"
