from django.db import models
from apps.consultations.models import Consultation
from apps.prescriptions.models import Prescription
# from apps.treatment_plans.models import TreatmentPlan
from apps.documents.models import Document
from apps.common.models import BaseModel
import uuid


class Report(BaseModel):

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    consultation = models.ForeignKey(
        "consultations.Consultation", on_delete=models.CASCADE, related_name="reports"
    )
    report_type = models.CharField(max_length=255)
    prescription_summary = models.ForeignKey(
        "prescriptions.Prescription",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports",
    )
    # treatment_plan_summary = models.ForeignKey(
    #     "treatment_plans.TreatmentPlan",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="reports",
    # )
    documents = models.ManyToManyField(
        "documents.Document", related_name="reports", blank=True
    )
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "reports"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Report for {self.consultation.consultation_number} - {self.report_type}"
        )
