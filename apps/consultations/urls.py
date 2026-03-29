from django.urls import path

from apps.consultations.views import (
    ConsultationListCreateAPIView,
    ConsultationDetailAPIView,
)

urlpatterns = [
    path("", ConsultationListCreateAPIView.as_view(), name="consultation-list-create"),
    path(
        "<uuid:consultation_id>/",
        ConsultationDetailAPIView.as_view(),
        name="consultation-detail",
    ),
]
