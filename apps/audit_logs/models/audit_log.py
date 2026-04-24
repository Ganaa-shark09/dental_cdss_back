from django.db import models
from django.contrib.auth import get_user_model
import uuid

from apps.common.models import BaseModel


class AuditLog(BaseModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    model_name = models.CharField(max_length=255, db_index=True)
    record_id = models.UUIDField(db_index=True)
    field_name = models.CharField(max_length=255, db_index=True)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.model_name} - {self.field_name} changed by {self.user}"
