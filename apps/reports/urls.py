from django.urls import path
from apps.reports.views.report import ReportListCreateAPIView, ReportDetailAPIView

urlpatterns = [
    path("", ReportListCreateAPIView.as_view(), name="report-list-create"),
    path("<uuid:report_id>/", ReportDetailAPIView.as_view(), name="report-detail"),
]
