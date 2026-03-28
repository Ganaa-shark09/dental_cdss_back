from django.db import models

from apps.common.models import BaseModel
import uuid


class Patient(BaseModel):
    GENDER_MALE = "MALE"
    GENDER_FEMALE = "FEMALE"
    GENDER_OTHER = "OTHER"

    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    ]

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    patient_code = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    blood_group = models.CharField(max_length=10, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    occupation = models.CharField(max_length=150, blank=True, null=True)

    emergency_contact_name = models.CharField(max_length=150, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "patients"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient_code} - {self.first_name} {self.last_name or ''}".strip()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name or ''}".strip()
