from rest_framework.exceptions import ValidationError

from apps.audit_logs.models import AuditLog


class AuditLogService:
    @staticmethod
    def normalize_value(value):
        if value is None:
            return None
        if isinstance(value, (dict, list, tuple, set)):
            return str(value)
        return str(value)

    @classmethod
    def create_log(cls, model_name, record_id, field_name, old_value, new_value, user):
        """
        Creates an audit log entry to track field-level changes.
        """
        return AuditLog.objects.create(
            model_name=model_name,
            record_id=record_id,
            field_name=field_name,
            old_value=cls.normalize_value(old_value),
            new_value=cls.normalize_value(new_value),
            user=user,
        )

    @staticmethod
    def get_logs(filters=None):
        """
        Retrieves all audit logs ordered by timestamp, with optional filtering.
        """
        queryset = AuditLog.objects.select_related("user").all().order_by("-timestamp")

        if not filters:
            return queryset

        model_name = filters.get("model_name")
        record_id = filters.get("record_id")
        field_name = filters.get("field_name")
        user_id = filters.get("user_id")

        if model_name:
            queryset = queryset.filter(model_name__iexact=model_name)

        if record_id:
            queryset = queryset.filter(record_id=record_id)

        if field_name:
            queryset = queryset.filter(field_name__iexact=field_name)

        if user_id:
            queryset = queryset.filter(user__id=user_id)

        return queryset

    @staticmethod
    def get_log_by_uuid(audit_log_uuid):
        try:
            return AuditLog.objects.select_related("user").get(uuid=audit_log_uuid)
        except AuditLog.DoesNotExist:
            raise ValidationError({"audit_log_uuid": ["Audit log not found."]})
