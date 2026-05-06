from datetime import date

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.appointments.models import Appointment
from apps.audit_logs.services import AuditLogService
from apps.patients.models import Patient
from apps.clinics.models import Clinic
from apps.staff.models import StaffProfile


class AppointmentService:
    APPOINTMENT_NUMBER_PREFIX = "APT"
    APPOINTMENT_NUMBER_PADDING = 5

    @staticmethod
    def get_patient(patient_uuid):
        try:
            return Patient.objects.get(uuid=patient_uuid, is_active=True)
        except Patient.DoesNotExist:
            raise ValidationError({"patient_id": ["Valid active patient not found."]})

    @staticmethod
    def get_clinic(clinic_uuid):
        try:
            return Clinic.objects.get(uuid=clinic_uuid, is_active=True)
        except Clinic.DoesNotExist:
            raise ValidationError({"clinic_id": ["Valid active clinic not found."]})

    @staticmethod
    def get_staff_profile(staff_profile_uuid):
        if not staff_profile_uuid:
            return None

        try:
            return StaffProfile.objects.select_related("clinic").get(
                uuid=staff_profile_uuid,
                is_active=True,
            )
        except StaffProfile.DoesNotExist:
            raise ValidationError(
                {"staff_profile_id": ["Valid active staff profile not found."]}
            )

    @classmethod
    def build_appointment_number(cls, appointment_id: int) -> str:
        return (
            f"{cls.APPOINTMENT_NUMBER_PREFIX}"
            f"{str(appointment_id).zfill(cls.APPOINTMENT_NUMBER_PADDING)}"
        )

    @staticmethod
    def validate_appointment_date(appointment_date):
        if appointment_date < date.today():
            raise ValidationError(
                {"appointment_date": ["Appointment date cannot be in the past."]}
            )

    @staticmethod
    def validate_staff_clinic_match(staff_profile, clinic):
        if staff_profile and staff_profile.clinic_id != clinic.id:
            raise ValidationError(
                {
                    "staff_profile_id": [
                        "Selected staff profile does not belong to the selected clinic."
                    ]
                }
            )

    @staticmethod
    def validate_duplicate_slot(patient, appointment_date, appointment_time):
        if Appointment.objects.filter(
            patient=patient,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            is_active=True,
        ).exists():
            raise ValidationError(
                {
                    "non_field_errors": [
                        "This patient already has an appointment at the same date and time."
                    ]
                }
            )

    @classmethod
    @transaction.atomic
    def create_appointment(cls, validated_data, user):
        patient = cls.get_patient(validated_data["patient_id"])
        clinic = cls.get_clinic(validated_data["clinic_id"])
        staff_profile = cls.get_staff_profile(validated_data.get("staff_profile_id"))

        appointment_date = validated_data["appointment_date"]
        appointment_time = validated_data["appointment_time"]

        cls.validate_appointment_date(appointment_date)
        cls.validate_staff_clinic_match(staff_profile, clinic)
        cls.validate_duplicate_slot(patient, appointment_date, appointment_time)

        appointment = Appointment.objects.create(
            patient=patient,
            clinic=clinic,
            staff_profile=staff_profile,
            appointment_number="TEMP",
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status=validated_data.get("status", Appointment.STATUS_SCHEDULED),
            reason_for_visit=validated_data.get("reason_for_visit", "").strip() or None,
            notes=validated_data.get("notes", "").strip() or None,
            is_active=validated_data.get("is_active", True),
        )

        appointment.appointment_number = cls.build_appointment_number(appointment.id)
        appointment.save(update_fields=["appointment_number"])

        AuditLogService.create_log(
            model_name="Appointment",
            record_id=appointment.uuid,
            field_name="created",
            old_value=None,
            new_value=appointment.appointment_number,
            user=user,
        )

        return appointment

    @staticmethod
    def list_appointments():
        return (
            Appointment.objects.select_related(
                "patient",
                "clinic",
                "staff_profile",
                "staff_profile__user",
            )
            .all()
            .order_by("-appointment_date", "-appointment_time")
        )

    @staticmethod
    def get_appointment_by_id(appointment_uuid):
        try:
            return Appointment.objects.select_related(
                "patient",
                "clinic",
                "staff_profile",
                "staff_profile__user",
            ).get(uuid=appointment_uuid)
        except Appointment.DoesNotExist:
            raise ValidationError({"appointment_id": ["Appointment not found."]})
