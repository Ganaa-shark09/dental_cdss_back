from django.core.management.base import BaseCommand
from apps.users.services import RoleService


class Command(BaseCommand):
    help = "Seed default roles"

    def handle(self, *args, **options):
        roles = RoleService.seed_roles()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully seeded {len(roles)} roles.")
        )
