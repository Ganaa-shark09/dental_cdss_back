from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "uuid",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "role",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
        )

    def get_role(self, obj):
        if not obj.role:
            return None

        return {
            "uuid": str(obj.role.uuid),
            "name": obj.role.name,
            "code": obj.role.code,
        }
