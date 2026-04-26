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
    def validate_username_uniqueness_for_update(username: str, user_uuid):
        if (
            User.objects.filter(username__iexact=username)
            .exclude(uuid=user_uuid)
            .exists()
        ):
            raise ValidationError(
                {"username": ["A user with this username already exists."]}
            )

    @staticmethod
    def validate_email_uniqueness_for_update(email: str, user_uuid):
        if User.objects.filter(email__iexact=email).exclude(uuid=user_uuid).exists():
            raise ValidationError({"email": ["A user with this email already exists."]})

    @staticmethod
    def get_role_by_uuid(role_uuid):
        if not role_uuid:
            return None

        try:
            return Role.objects.get(uuid=role_uuid, is_active=True)
        except Role.DoesNotExist:
            raise ValidationError({"role_id": ["Valid active role not found."]})

    @staticmethod
    def get_user_by_uuid(user_uuid):
        try:
            return User.objects.select_related("role").get(uuid=user_uuid)
        except User.DoesNotExist:
            raise ValidationError({"user_uuid": ["User not found."]})

    @classmethod
    @transaction.atomic
    def create_user(cls, validated_data):
        username = validated_data["username"].strip()
        email = validated_data["email"].strip().lower()

        cls.validate_username_uniqueness(username)
        cls.validate_email_uniqueness(email)

        role = cls.get_role_by_uuid(validated_data.get("role_id"))

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data["password"],
            first_name=validated_data["first_name"].strip(),
            last_name=validated_data.get("last_name", "").strip() or "",
            phone_number=validated_data.get("phone_number", "").strip() or "",
            role=role,
            is_active=validated_data.get("is_active", True),
            is_staff=validated_data.get("is_staff", False),
        )
        return user

    @classmethod
    @transaction.atomic
    def update_user(cls, user_uuid, validated_data):
        user = cls.get_user_by_uuid(user_uuid)

        if "username" in validated_data:
            username = validated_data["username"].strip()
            cls.validate_username_uniqueness_for_update(username, user_uuid)
            user.username = username

        if "email" in validated_data:
            email = validated_data["email"].strip().lower()
            cls.validate_email_uniqueness_for_update(email, user_uuid)
            user.email = email

        if "first_name" in validated_data:
            user.first_name = validated_data["first_name"].strip()

        if "last_name" in validated_data:
            user.last_name = validated_data.get("last_name", "").strip() or None

        if "phone_number" in validated_data:
            user.phone_number = validated_data.get("phone_number", "").strip() or None

        if "role_id" in validated_data:
            user.role = cls.get_role_by_uuid(validated_data.get("role_id"))

        if "is_active" in validated_data:
            user.is_active = validated_data["is_active"]

        if "is_staff" in validated_data:
            user.is_staff = validated_data["is_staff"]

        user.save()
        return user

    @staticmethod
    def list_users():
        return User.objects.select_related("role").all().order_by("-created_at")

    @staticmethod
    def list_roles():
        return Role.objects.filter(is_active=True).order_by("name")
