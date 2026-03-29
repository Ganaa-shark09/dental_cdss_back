from django.db import models

from apps.common.models import BaseModel
from apps.cdss.models import CdssEngine
import uuid


class CdssRecommendation(BaseModel):

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    cdss_engine = models.ForeignKey(
        "cdss.CdssEngine", on_delete=models.CASCADE, related_name="cdss_recommendations"
    )
    recommendation = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "cdss_recommendations"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Recommendation for {self.cdss_engine.consultation.consultation_number}"
