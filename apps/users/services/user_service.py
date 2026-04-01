from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.users.models import User, Role


class UserService:
    @staticmethod
    def validate_username_uniqueness(username: str):
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError(
                {"username": ["A user with this username already exists."]}
            )

    @staticmethod
    def validate_email_uniqueness(email: str):
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError({"email": ["A user with this email already exists."]})

    @staticmethod
    def get_role_by_id(role_id):
        if not role_id:
            return None

        try:
            return Role.objects.get(id=role_id, is_active=True)
        except Role.DoesNotExist:
            raise ValidationError({"role_id": ["Valid active role not found."]})

    @classmethod
    @transaction.atomic
    def create_user(cls, validated_data):
        username = validated_data["username"].strip()
        email = validated_data["email"].strip().lower()

        cls.validate_username_uniqueness(username)
        cls.validate_email_uniqueness(email)

        role = cls.get_role_by_id(validated_data.get("role_id"))

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data.get("last_name", ""),
            phone_number=validated_data.get("phone_number", ""),
            role=role,
            is_active=validated_data.get("is_active", True),
            is_staff=validated_data.get("is_staff", False),
        )
        return user

    @staticmethod
    def list_users():
        return User.objects.select_related("role").all().order_by("-created_at")

    @staticmethod
    def list_roles():
        return Role.objects.filter(is_active=True).order_by("name")
