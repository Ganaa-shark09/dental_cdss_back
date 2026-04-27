import uuid

from django.db import models

from apps.common.models import BaseModel


class CdssEngine(BaseModel):

    DEPT_GENERAL = "GENERAL"
    DEPT_ENDODONTICS = "ENDODONTICS"
    DEPT_PERIODONTICS = "PERIODONTICS"
    DEPT_ORAL_SURGERY = "ORAL_SURGERY"
    DEPT_ORTHODONTICS = "ORTHODONTICS"
    DEPT_PROSTHODONTICS = "PROSTHODONTICS"
    DEPT_PEDIATRIC = "PEDIATRIC"
    DEPT_PREVENTIVE = "PREVENTIVE"

    DEPT_CHOICES = [
        (DEPT_GENERAL, "General Dentistry"),
        (DEPT_ENDODONTICS, "Endodontics"),
        (DEPT_PERIODONTICS, "Periodontics"),
        (DEPT_ORAL_SURGERY, "Oral Surgery"),
        (DEPT_ORTHODONTICS, "Orthodontics"),
        (DEPT_PROSTHODONTICS, "Prosthodontics"),
        (DEPT_PEDIATRIC, "Pediatric Dentistry"),
        (DEPT_PREVENTIVE, "Preventive Dentistry"),
    ]

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    consultation = models.OneToOneField(
        "consultations.Consultation", on_delete=models.CASCADE, related_name="cdss"
    )
    department = models.CharField(
        max_length=30,
        choices=DEPT_CHOICES,
        default=DEPT_GENERAL,
    )
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    alerts = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    diagnosis_assistance = models.TextField(blank=True, null=True)
    # Structured engine output fields
    icd_code = models.CharField(max_length=20, blank=True, null=True)
    confidence = models.CharField(max_length=20, blank=True, null=True)
    per_tooth_results = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "cdss_engines"
        ordering = ["-created_at"]

    def __str__(self):
        return f"CDSS Engine for {self.consultation.consultation_number}"
