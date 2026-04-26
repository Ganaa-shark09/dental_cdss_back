from rest_framework import serializers

from apps.users.models import Role, User


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            "uuid",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )
