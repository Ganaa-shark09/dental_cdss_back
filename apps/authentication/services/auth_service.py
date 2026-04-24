from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class AuthService:
    @staticmethod
    def login_user(username: str, password: str):
        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed("Invalid username or password.")

        if not user.is_active:
            raise AuthenticationFailed("This user account is inactive.")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.full_name,
                "role": user.role.name if user.role else None,
            },
        }

    @staticmethod
    def change_password(user, old_password: str, new_password: str):
        if not user.check_password(old_password):
            raise AuthenticationFailed("Old password is incorrect.")

        user.set_password(new_password)
        user.save(update_fields=["password"])
        return user
