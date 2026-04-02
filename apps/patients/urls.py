from django.urls import path
from apps.patients.views import PatientListCreateAPIView, PatientDetailAPIView

urlpatterns = [
    path("", PatientListCreateAPIView.as_view(), name="patient-list-create"),
    path("<uuid:patient_uuid>/", PatientDetailAPIView.as_view(), name="patient-detail"),
]
