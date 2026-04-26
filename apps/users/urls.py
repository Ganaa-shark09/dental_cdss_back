from django.urls import path

from apps.users.views import (
    RoleListAPIView,
    UserListCreateAPIView,
    MeAPIView,
)
from apps.users.views.user_management import UserDetailAPIView

urlpatterns = [
    path("roles/", RoleListAPIView.as_view(), name="role-list"),
    path("users/", UserListCreateAPIView.as_view(), name="user-list-create"),
    path("users/<uuid:user_uuid>/", UserDetailAPIView.as_view(), name="user-detail"),
    path("users/me/", MeAPIView.as_view(), name="me"),
]