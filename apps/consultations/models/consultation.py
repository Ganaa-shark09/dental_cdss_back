from django.db import models

from apps.common.models import BaseModel
import uuid


class Consultation(BaseModel):
    STATUS_DRAFT = "DRAFT"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(
        "appointments.Appointment",
        on_delete=models.SET_NULL,
        related_name="consultation",
        blank=True,
        null=True,
    )
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="consultations",
    )
    clinic = models.ForeignKey(
        "clinics.Clinic",
        on_delete=models.CASCADE,
        related_name="consultations",
    )
    staff_profile = models.ForeignKey(
        "staff.StaffProfile",
        on_delete=models.SET_NULL,
        related_name="consultations",
        blank=True,
        null=True,
    )

    consultation_number = models.CharField(max_length=50, unique=True)
    consultation_date = models.DateField()
    consultation_time = models.TimeField()

    chief_complaint = models.TextField(blank=True, null=True)
    history_of_present_illness = models.TextField(blank=True, null=True)
    medical_history_summary = models.TextField(blank=True, null=True)
    dental_history_summary = models.TextField(blank=True, null=True)
    examination_summary = models.TextField(blank=True, null=True)

    # Structured wizard fields
    systemic_conditions = models.JSONField(default=list, blank=True)
    habits = models.JSONField(default=list, blank=True)
    allergies = models.JSONField(default=list, blank=True)
    current_medications = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    hospitalization_history = models.TextField(blank=True, null=True)
    past_dental_history = models.JSONField(default=list, blank=True)
    complaint_duration = models.CharField(max_length=50, blank=True, null=True)
    complaint_severity = models.CharField(max_length=20, blank=True, null=True)
    visit_number = models.CharField(max_length=50, blank=True, null=True)
    opd_number = models.CharField(max_length=50, blank=True, null=True)
    reference = models.CharField(max_length=200, blank=True, null=True)

    provisional_diagnosis = models.TextField(blank=True, null=True)
    final_diagnosis = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "consultations"
        ordering = ["-consultation_date", "-consultation_time"]

    def __str__(self):
        return f"{self.consultation_number} - {self.patient.full_name}"
