from django.db import models

from apps.common.models import BaseModel
import uuid


class DentalChart(BaseModel):

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    consultation = models.OneToOneField(
        "consultations.Consultation",
        on_delete=models.CASCADE,
        related_name="dental_chart",
    )
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "dental_charts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Dental Chart - {self.consultation.consultation_number}"
