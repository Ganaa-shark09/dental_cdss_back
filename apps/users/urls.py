from django.urls import path
from apps.users.views import MeAPIView, RoleListAPIView, UserListCreateAPIView

urlpatterns = [
    path("me/", MeAPIView.as_view(), name="me"),
    path("roles/", RoleListAPIView.as_view(), name="role-list"),
    path("", UserListCreateAPIView.as_view(), name="user-list-create"),
]
