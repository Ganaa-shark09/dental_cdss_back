from apps.users.models import Role


class RoleService:
    DEFAULT_ROLES = [
        {
            "name": "Super Admin",
            "code": "SUPER_ADMIN",
            "description": "System-wide super administrator",
        },
        {
            "name": "Clinic Admin",
            "code": "CLINIC_ADMIN",
            "description": "Clinic administrator with management access",
        },
        {
            "name": "Dentist",
            "code": "DENTIST",
            "description": "Dental practitioner",
        },
        {
            "name": "Assistant",
            "code": "ASSISTANT",
            "description": "Dental assistant",
        },
        {
            "name": "Receptionist",
            "code": "RECEPTIONIST",
            "description": "Front desk and appointment handling staff",
        },
    ]

    @classmethod
    def seed_roles(cls):
        created_roles = []

        for role_data in cls.DEFAULT_ROLES:
            role, _ = Role.objects.get_or_create(
                code=role_data["code"],
                defaults={
                    "name": role_data["name"],
                    "description": role_data["description"],
                    "is_active": True,
                },
            )
            created_roles.append(role)

        return created_roles
