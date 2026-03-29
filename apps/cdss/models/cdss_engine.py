from django.db import models

from apps.common.models import BaseModel
from apps.consultations.models import Consultation
import uuid


class CdssEngine(BaseModel):

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    consultation = models.OneToOneField(
        "consultations.Consultation", on_delete=models.CASCADE, related_name="cdss"
    )
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    alerts = models.JSONField(default=list, blank=True)  # Alerts/Warnings
    recommendations = models.JSONField(default=list, blank=True)  # Suggested treatments
    diagnosis_assistance = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "cdss_engines"
        ordering = ["-created_at"]

    def __str__(self):
        return f"CDSS Engine for {self.consultation.consultation_number}"
