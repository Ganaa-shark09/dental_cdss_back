from django.db import models

from apps.common.models import BaseModel
from django.contrib.auth import get_user_model


class AuditLog(BaseModel):
    model_name = models.CharField(max_length=255)
    record_id = models.UUIDField()
    field_name = models.CharField(max_length=255)
    old_value = models.TextField()
    new_value = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.model_name} - {self.field_name} changed by {self.user}"
