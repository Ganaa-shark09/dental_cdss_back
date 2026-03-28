from django.urls import path

from apps.appointments.views import (
    AppointmentListCreateAPIView,
    AppointmentDetailAPIView,
)

urlpatterns = [
    path("", AppointmentListCreateAPIView.as_view(), name="appointment-list-create"),
    path(
        "<uuid:appointment_id>/",
        AppointmentDetailAPIView.as_view(),
        name="appointment-detail",
    ),
]
