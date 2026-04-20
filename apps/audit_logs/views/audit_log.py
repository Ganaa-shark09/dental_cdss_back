from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit_logs.serializers import AuditLogSerializer
from apps.audit_logs.services import AuditLogService


class AuditLogListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        filters = {
            "model_name": request.query_params.get("model_name"),
            "record_id": request.query_params.get("record_id"),
            "field_name": request.query_params.get("field_name"),
            "user_id": request.query_params.get("user_id"),
        }

        logs = AuditLogService.get_logs(filters=filters)
        serializer = AuditLogSerializer(logs, many=True)
        return Response(serializer.data)


class AuditLogDetailAPIView(APIView):
    def get(self, request, audit_log_uuid, *args, **kwargs):
        log = AuditLogService.get_log_by_uuid(audit_log_uuid)
        serializer = AuditLogSerializer(log)
        return Response(serializer.data)
