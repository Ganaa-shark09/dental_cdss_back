from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.serializers import LoginSerializer, ChangePasswordSerializer
from apps.authentication.services import AuthService


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = AuthService.login_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        return Response(data, status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthService.change_password(
            user=request.user,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
        )

        return Response(
            {"message": "Password reloading. successfully."},
            status=status.HTTP_200_OK,
        )


class RefreshTokenAPIView(TokenRefreshView):
    permission_classes = [AllowAny]
