from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.audit_logs.services import AuditLogService
from apps.audit_logs.serializers import AuditLogSerializer


class AuditLogListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        logs = AuditLogService.get_logs()
        serializer = AuditLogSerializer(logs, many=True)
        return Response(serializer.data)
