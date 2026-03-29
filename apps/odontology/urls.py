from django.urls import path

from apps.odontology.views import (
    DentalChartListCreateAPIView,
    DentalChartDetailAPIView,
    ToothRecordListCreateAPIView,
)

urlpatterns = [
    path("", DentalChartListCreateAPIView.as_view(), name="dental-chart-list-create"),
    path(
        "<uuid:chart_id>/",
        DentalChartDetailAPIView.as_view(),
        name="dental-chart-detail",
    ),
    path(
        "<uuid:chart_id>/tooth-records/",
        ToothRecordListCreateAPIView.as_view(),
        name="tooth-record-list-create",
    ),
]
