from django.urls import path
from apps.audit_logs.views import AuditLogListAPIView, AuditLogDetailAPIView

urlpatterns = [
    path("", AuditLogListAPIView.as_view(), name="audit-log-list"),
    path(
        "<uuid:audit_log_uuid>/",
        AuditLogDetailAPIView.as_view(),
        name="audit-log-detail",
    ),
]
