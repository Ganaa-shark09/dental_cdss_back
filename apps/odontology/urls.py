from django.urls import path

from apps.odontology.views import (
    DentalChartListCreateAPIView,
    DentalChartDetailAPIView,
    ToothRecordListCreateAPIView,
    ToothRecordDetailAPIView,
)

urlpatterns = [
    path(
        "",
        DentalChartListCreateAPIView.as_view(),
        name="dental-chart-list-create",
    ),
    path(
        "<uuid:chart_uuid>/",
        DentalChartDetailAPIView.as_view(),
        name="dental-chart-detail",
    ),
    path(
        "<uuid:chart_uuid>/tooth-records/",
        ToothRecordListCreateAPIView.as_view(),
        name="tooth-record-list-create",
    ),
    path(
        "<uuid:chart_uuid>/tooth-records/<uuid:tooth_record_uuid>/",
        ToothRecordDetailAPIView.as_view(),
        name="tooth-record-detail",
    ),
]
