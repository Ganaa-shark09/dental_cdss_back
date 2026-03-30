from django.db import models

from apps.common.models import BaseModel
from apps.consultations.models import Consultation
import uuid


class TreatmentPlan(BaseModel):
    STATUS_PLANNED = "PLANNED"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_COMPLETED = "COMPLETED"

    STATUS_CHOICES = [
        (STATUS_PLANNED, "Planned"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
    ]

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    consultation = models.ForeignKey(
        "consultations.Consultation",
        on_delete=models.CASCADE,
        related_name="treatment_plans",
    )
    treatment_type = models.CharField(max_length=255)
    treatment_description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PLANNED
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "treatment_plans"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Treatment Plan for {self.consultation.consultation_number} - {self.treatment_type}"
