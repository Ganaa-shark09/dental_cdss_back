from django.db import models

from apps.common.models import BaseModel
import uuid
from apps.clinics.models import Clinic


class StaffProfile(BaseModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name="staff_profiles",
    )
    employee_id = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=100)
    specialization = models.CharField(max_length=150, blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "staff_profiles"
        ordering = ["designation", "employee_id"]

    def __str__(self):
        return f"{self.user.full_name} - {self.designation}"
