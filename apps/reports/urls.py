from django.urls import path
from apps.reports.views import ReportListCreateAPIView, ReportDetailAPIView

urlpatterns = [
    path("", ReportListCreateAPIView.as_view(), name="report-list-create"),
    path(
        "<uuid:report_uuid>/",
        ReportDetailAPIView.as_view(),
        name="report-detail",
    ),
]
