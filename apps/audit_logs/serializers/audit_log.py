from rest_framework import serializers
from apps.audit_logs.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = (
            "uuid",
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

    def get_user(self, obj):
        if not obj.user:
            return None

        return {
            "id": obj.user.id,
            "uuid": (
                str(obj.user.uuid)
                if hasattr(obj.user, "uuid") and obj.user.uuid
                else None
            ),
            "email": getattr(obj.user, "email", None),
            "full_name": getattr(obj.user, "full_name", None),
        }
