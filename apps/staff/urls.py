from django.urls import path
from apps.staff.views import StaffProfileListCreateAPIView

urlpatterns = [
    path("", StaffProfileListCreateAPIView.as_view(), name="staff-profile-list-create"),
]
