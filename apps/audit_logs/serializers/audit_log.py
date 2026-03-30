from rest_framework import serializers
from apps.audit_logs.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = (
            "id",
            "model_name",
            "record_id",
            "field_name",
            "old_value",
            "new_value",
            "user",
            "timestamp",
            "created_at",
            "updated_at",
        )
