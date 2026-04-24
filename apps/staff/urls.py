from django.urls import path
from apps.staff.views import StaffProfileListCreateAPIView
from apps.staff.views.staff_profile import StaffProfileDetailAPIView

urlpatterns = [
    path("", StaffProfileListCreateAPIView.as_view(), name="staff-profile-list-create"),
    path(
        "<uuid:staff_uuid>/",
        StaffProfileDetailAPIView.as_view(),
        name="staff-detail",
    ),
]
