from django.urls import path
from apps.prescriptions.views.prescription import (
    PrescriptionListCreateAPIView,
    PrescriptionDetailAPIView,
    PrescriptionPrintAPIView,
)

urlpatterns = [
    path("", PrescriptionListCreateAPIView.as_view(), name="prescription-list-create"),
    path(
        "<uuid:prescription_uuid>/",
        PrescriptionDetailAPIView.as_view(),
        name="prescription-detail",
    ),
    path(
        "<uuid:prescription_uuid>/print/",
        PrescriptionPrintAPIView.as_view(),
        name="prescription-print",
    ),
]
