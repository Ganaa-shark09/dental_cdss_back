from django.urls import path
from apps.clinics.views import ClinicListCreateAPIView

urlpatterns = [
    path("", ClinicListCreateAPIView.as_view(), name="clinic-list-create"),
]
