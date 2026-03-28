from django.urls import path
from apps.authentication.views import (
    LoginAPIView,
    ChangePasswordAPIView,
    RefreshTokenAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", RefreshTokenAPIView.as_view(), name="token_refresh"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change_password"),
]
