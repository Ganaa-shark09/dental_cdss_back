from django.db import models

from apps.common.models import BaseModel
import uuid


class ToothRecord(BaseModel):
    CONDITION_SOUND = "SOUND"
    CONDITION_CARIES = "CARIES"
    CONDITION_FILLED = "FILLED"
    CONDITION_MISSING = "MISSING"
    CONDITION_FRACTURED = "FRACTURED"
    CONDITION_MOBILE = "MOBILE"
    CONDITION_ROOT_STUMP = "ROOT_STUMP"
    CONDITION_IMPACTED = "IMPACTED"
    CONDITION_ATTRITION = "ATTRITION"
    CONDITION_ABRASION = "ABRASION"
    CONDITION_ABFRACTION = "ABFRACTION"
    CONDITION_DISCOLORED = "DISCOLORED"

    CONDITION_CHOICES = [
        (CONDITION_SOUND, "Sound"),
        (CONDITION_CARIES, "Caries"),
        (CONDITION_FILLED, "Filled"),
        (CONDITION_MISSING, "Missing"),
        (CONDITION_FRACTURED, "Fractured"),
        (CONDITION_MOBILE, "Mobile"),
        (CONDITION_ROOT_STUMP, "Root Stump"),
        (CONDITION_IMPACTED, "Impacted"),
        (CONDITION_ATTRITION, "Attrition"),
        (CONDITION_ABRASION, "Abrasion"),
        (CONDITION_ABFRACTION, "Abfraction"),
        (CONDITION_DISCOLORED, "Discolored"),
    ]

    SURFACE_MESIAL = "MESIAL"
    SURFACE_DISTAL = "DISTAL"
    SURFACE_OCCLUSAL = "OCCLUSAL"
    SURFACE_BUCCAL = "BUCCAL"
    SURFACE_LINGUAL = "LINGUAL"
    SURFACE_LABIAL = "LABIAL"
    SURFACE_INCISAL = "INCISAL"
    SURFACE_CERVICAL = "CERVICAL"

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    chart = models.ForeignKey(
        "odontology.DentalChart",
        on_delete=models.CASCADE,
        related_name="tooth_records",
    )
    tooth_number = models.CharField(max_length=10)
    condition = models.CharField(
        max_length=30,
        choices=CONDITION_CHOICES,
    )
    surfaces = models.JSONField(default=list, blank=True)
    mobility_grade = models.CharField(max_length=20, blank=True, null=True)
    percussion_tenderness = models.BooleanField(default=False)
    palpation_tenderness = models.BooleanField(default=False)
    probing_depth_summary = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    # Adaptive exam data: all department-specific examination fields from the wizard
    # Structure mirrors the CLINICAL_SCHEMA fields (coldResponse, percussion, etc.)
    exam_data = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "tooth_records"
        ordering = ["tooth_number"]
        unique_together = ("chart", "tooth_number")

    def __str__(self):
        return f"{self.tooth_number} - {self.condition}"
