from django.urls import path
from apps.clinics.views import ClinicListCreateAPIView, ClinicDetailAPIView

urlpatterns = [
    path("", ClinicListCreateAPIView.as_view(), name="clinic-list-create"),
    path("<uuid:uuid>/", ClinicDetailAPIView.as_view(), name="clinic-detail"),
]
