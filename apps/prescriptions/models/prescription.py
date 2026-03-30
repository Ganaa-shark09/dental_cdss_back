from django.db import models

from apps.common.models import BaseModel
from apps.consultations.models import Consultation
from apps.patients.models import Patient
import uuid


class Prescription(BaseModel):

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    consultation = models.ForeignKey(
        "consultations.Consultation",
        on_delete=models.CASCADE,
        related_name="prescriptions",
    )
    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.CASCADE, related_name="prescriptions"
    )
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    treatment_instructions = models.TextField()
    notes = models.TextField(blank=True, null=True)
    date_issued = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "prescriptions"
        ordering = ["-date_issued"]

    def __str__(self):
        return f"Prescription for {self.patient.full_name} - {self.medication}"
