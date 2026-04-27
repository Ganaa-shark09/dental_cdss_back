import uuid

from django.db import models

from apps.common.models import BaseModel


class ToothComplaint(BaseModel):
    """
    Stores tooth-wise structured complaint codes submitted through the wizard.
    Each row = one tooth selected by the patient during the Chief Complaint step.
    complaint_codes stores a list of dicts:
      [{"code": "ENDO_COLD_PAIN", "complaint": "Sensitivity to cold", "department": "ENDO"}, ...]
    """

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    consultation = models.ForeignKey(
        "consultations.Consultation",
        on_delete=models.CASCADE,
        related_name="tooth_complaints",
    )
    tooth_number = models.CharField(max_length=10)
    complaint_codes = models.JSONField(default=list, blank=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    severity = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "tooth_complaints"
        ordering = ["tooth_number"]
        unique_together = ("consultation", "tooth_number")

    def __str__(self):
        return f"Tooth {self.tooth_number} - {self.consultation.consultation_number}"
