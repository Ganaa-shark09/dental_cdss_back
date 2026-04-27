from django.urls import path

from apps.consultations.views import (
    ConsultationListCreateAPIView,
    ConsultationDetailAPIView,
    ToothComplaintListCreateAPIView,
    ToothComplaintBulkAPIView,
    ToothComplaintDetailAPIView,
)

urlpatterns = [
    path("", ConsultationListCreateAPIView.as_view(), name="consultation-list-create"),
    path(
        "<uuid:consultation_id>/",
        ConsultationDetailAPIView.as_view(),
        name="consultation-detail",
    ),
    path(
        "<uuid:consultation_id>/tooth-complaints/",
        ToothComplaintListCreateAPIView.as_view(),
        name="tooth-complaint-list-create",
    ),
    path(
        "<uuid:consultation_id>/tooth-complaints/bulk/",
        ToothComplaintBulkAPIView.as_view(),
        name="tooth-complaint-bulk",
    ),
    path(
        "<uuid:consultation_id>/tooth-complaints/<uuid:tooth_complaint_id>/",
        ToothComplaintDetailAPIView.as_view(),
        name="tooth-complaint-detail",
    ),
]
