from django.db import models

from apps.common.models import BaseModel
import uuid


class Appointment(BaseModel):
    STATUS_SCHEDULED = "SCHEDULED"
    STATUS_CONFIRMED = "CONFIRMED"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_NO_SHOW = "NO_SHOW"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_NO_SHOW, "No Show"),
    ]

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    clinic = models.ForeignKey(
        "clinics.Clinic",
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    staff_profile = models.ForeignKey(
        "staff.StaffProfile",
        on_delete=models.SET_NULL,
        related_name="appointments",
        blank=True,
        null=True,
    )

    appointment_number = models.CharField(max_length=50, unique=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SCHEDULED,
    )

    reason_for_visit = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "appointments"
        ordering = ["-appointment_date", "-appointment_time"]

    def __str__(self):
        return f"{self.appointment_number} - {self.patient.full_name}"
