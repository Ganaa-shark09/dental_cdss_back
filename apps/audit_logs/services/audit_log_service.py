from apps.audit_logs.models import AuditLog


class AuditLogService:
    @staticmethod
    def create_log(model_name, record_id, field_name, old_value, new_value, user):
        """
        Creates an audit log entry to track changes.
        """
        AuditLog.objects.create(
            model_name=model_name,
            record_id=record_id,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            user=user,
        )

    @staticmethod
    def get_logs():
        """
        Retrieves all the audit logs ordered by timestamp.
        """
        return AuditLog.objects.all().order_by("-timestamp")
