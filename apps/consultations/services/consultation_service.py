from datetime import date

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.appointments.models import Appointment
from apps.audit_logs.services import AuditLogService
from apps.clinics.models import Clinic
from apps.consultations.models import Consultation
from apps.patients.models import Patient
from apps.staff.models import StaffProfile


class ConsultationService:
    CONSULTATION_NUMBER_PREFIX = "CON"
    CONSULTATION_NUMBER_PADDING = 5

    @staticmethod
    def get_appointment(appointment_uuid):
        if not appointment_uuid:
            return None

        try:
            return Appointment.objects.select_related(
                "patient",
                "clinic",
                "staff_profile",
            ).get(uuid=appointment_uuid, is_active=True)
        except Appointment.DoesNotExist:
            raise ValidationError(
                {"appointment_id": ["Valid active appointment not found."]}
            )

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
    def build_consultation_number(cls, consultation_id: int) -> str:
        return (
            f"{cls.CONSULTATION_NUMBER_PREFIX}"
            f"{str(consultation_id).zfill(cls.CONSULTATION_NUMBER_PADDING)}"
        )

    @staticmethod
    def validate_consultation_date(consultation_date):
        if consultation_date > date.today():
            raise ValidationError(
                {"consultation_date": ["Consultation date cannot be in the future."]}
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
    def validate_appointment_not_already_linked(appointment, current_consultation=None):
        if not appointment:
            return

        qs = Consultation.objects.filter(appointment=appointment)
        if current_consultation:
            qs = qs.exclude(uuid=current_consultation.uuid)

        if qs.exists():
            raise ValidationError(
                {
                    "appointment_id": [
                        "This appointment is already linked to a consultation."
                    ]
                }
            )

    @staticmethod
    def validate_appointment_consistency(appointment, patient, clinic, staff_profile):
        if not appointment:
            return

        if appointment.patient_id != patient.id:
            raise ValidationError(
                {
                    "patient_id": [
                        "Selected patient does not match the appointment patient."
                    ]
                }
            )

        if appointment.clinic_id != clinic.id:
            raise ValidationError(
                {
                    "clinic_id": [
                        "Selected clinic does not match the appointment clinic."
                    ]
                }
            )

        if (
            staff_profile
            and appointment.staff_profile_id
            and appointment.staff_profile_id != staff_profile.id
        ):
            raise ValidationError(
                {
                    "staff_profile_id": [
                        "Selected staff profile does not match the appointment staff profile."
                    ]
                }
            )

    @classmethod
    @transaction.atomic
    def create_consultation(cls, validated_data, user):
        appointment = cls.get_appointment(validated_data.get("appointment_id"))
        patient = cls.get_patient(validated_data["patient_id"])
        clinic = cls.get_clinic(validated_data["clinic_id"])
        staff_profile = cls.get_staff_profile(validated_data.get("staff_profile_id"))

        consultation_date = validated_data["consultation_date"]

        cls.validate_consultation_date(consultation_date)
        cls.validate_staff_clinic_match(staff_profile, clinic)
        cls.validate_appointment_not_already_linked(appointment)
        cls.validate_appointment_consistency(
            appointment, patient, clinic, staff_profile
        )

        consultation = Consultation.objects.create(
            appointment=appointment,
            patient=patient,
            clinic=clinic,
            staff_profile=staff_profile,
            consultation_number="TEMP",
            consultation_date=consultation_date,
            consultation_time=validated_data["consultation_time"],
            chief_complaint=validated_data.get("chief_complaint", "").strip() or None,
            history_of_present_illness=validated_data.get(
                "history_of_present_illness", ""
            ).strip()
            or None,
            medical_history_summary=validated_data.get(
                "medical_history_summary", ""
            ).strip()
            or None,
            dental_history_summary=validated_data.get(
                "dental_history_summary", ""
            ).strip()
            or None,
            examination_summary=validated_data.get("examination_summary", "").strip()
            or None,
            provisional_diagnosis=validated_data.get(
                "provisional_diagnosis", ""
            ).strip()
            or None,
            final_diagnosis=validated_data.get("final_diagnosis", "").strip() or None,
            notes=validated_data.get("notes", "").strip() or None,
            status=validated_data.get("status", Consultation.STATUS_DRAFT),
            is_active=validated_data.get("is_active", True),
        )

        consultation.consultation_number = cls.build_consultation_number(
            consultation.id
        )
        consultation.save(update_fields=["consultation_number"])

        AuditLogService.create_log(
            model_name="Consultation",
            record_id=consultation.uuid,
            field_name="created",
            old_value=None,
            new_value=consultation.consultation_number,
            user=user,
        )

        return consultation

    @staticmethod
    def list_consultations():
        return (
            Consultation.objects.select_related(
                "appointment",
                "patient",
                "clinic",
                "staff_profile",
                "staff_profile__user",
            )
            .all()
            .order_by("-consultation_date", "-consultation_time")
        )

    @staticmethod
    def get_consultation_by_id(consultation_uuid):
        try:
            return Consultation.objects.select_related(
                "appointment",
                "patient",
                "clinic",
                "staff_profile",
                "staff_profile__user",
            ).get(uuid=consultation_uuid)
        except Consultation.DoesNotExist:
            raise ValidationError({"consultation_id": ["Consultation not found."]})

    @classmethod
    @transaction.atomic
    def update_consultation(cls, consultation_uuid, validated_data, user):
        consultation = cls.get_consultation_by_id(consultation_uuid)

        # Capture old values before any modifications
        old_values = {
            "appointment": str(consultation.appointment.uuid) if consultation.appointment else None,
            "patient": str(consultation.patient.uuid),
            "clinic": str(consultation.clinic.uuid),
            "staff_profile": str(consultation.staff_profile.uuid) if consultation.staff_profile else None,
            "consultation_date": str(consultation.consultation_date),
            "consultation_time": str(consultation.consultation_time),
            "chief_complaint": consultation.chief_complaint,
            "history_of_present_illness": consultation.history_of_present_illness,
            "medical_history_summary": consultation.medical_history_summary,
            "dental_history_summary": consultation.dental_history_summary,
            "examination_summary": consultation.examination_summary,
            "provisional_diagnosis": consultation.provisional_diagnosis,
            "final_diagnosis": consultation.final_diagnosis,
            "notes": consultation.notes,
            "status": consultation.status,
            "is_active": consultation.is_active,
        }

        appointment = (
            cls.get_appointment(validated_data.get("appointment_id"))
            if "appointment_id" in validated_data
            else consultation.appointment
        )
        patient = (
            cls.get_patient(validated_data["patient_id"])
            if "patient_id" in validated_data
            else consultation.patient
        )
        clinic = (
            cls.get_clinic(validated_data["clinic_id"])
            if "clinic_id" in validated_data
            else consultation.clinic
        )
        staff_profile = (
            cls.get_staff_profile(validated_data.get("staff_profile_id"))
            if "staff_profile_id" in validated_data
            else consultation.staff_profile
        )
        consultation_date = validated_data.get(
            "consultation_date", consultation.consultation_date
        )

        cls.validate_consultation_date(consultation_date)
        cls.validate_staff_clinic_match(staff_profile, clinic)
        cls.validate_appointment_not_already_linked(appointment, consultation)
        cls.validate_appointment_consistency(
            appointment, patient, clinic, staff_profile
        )

        consultation.appointment = appointment
        consultation.patient = patient
        consultation.clinic = clinic
        consultation.staff_profile = staff_profile
        consultation.consultation_date = consultation_date
        consultation.consultation_time = validated_data.get(
            "consultation_time", consultation.consultation_time
        )

        if "chief_complaint" in validated_data:
            consultation.chief_complaint = (
                validated_data.get("chief_complaint", "").strip() or None
            )

        if "history_of_present_illness" in validated_data:
            consultation.history_of_present_illness = (
                validated_data.get("history_of_present_illness", "").strip() or None
            )

        if "medical_history_summary" in validated_data:
            consultation.medical_history_summary = (
                validated_data.get("medical_history_summary", "").strip() or None
            )

        if "dental_history_summary" in validated_data:
            consultation.dental_history_summary = (
                validated_data.get("dental_history_summary", "").strip() or None
            )

        if "examination_summary" in validated_data:
            consultation.examination_summary = (
                validated_data.get("examination_summary", "").strip() or None
            )

        if "provisional_diagnosis" in validated_data:
            consultation.provisional_diagnosis = (
                validated_data.get("provisional_diagnosis", "").strip() or None
            )

        if "final_diagnosis" in validated_data:
            consultation.final_diagnosis = (
                validated_data.get("final_diagnosis", "").strip() or None
            )

        if "notes" in validated_data:
            consultation.notes = validated_data.get("notes", "").strip() or None

        if "status" in validated_data:
            consultation.status = validated_data["status"]

        if "is_active" in validated_data:
            consultation.is_active = validated_data["is_active"]

        consultation.save()

        # Log each changed field
        new_values = {
            "appointment": str(consultation.appointment.uuid) if consultation.appointment else None,
            "patient": str(consultation.patient.uuid),
            "clinic": str(consultation.clinic.uuid),
            "staff_profile": str(consultation.staff_profile.uuid) if consultation.staff_profile else None,
            "consultation_date": str(consultation.consultation_date),
            "consultation_time": str(consultation.consultation_time),
            "chief_complaint": consultation.chief_complaint,
            "history_of_present_illness": consultation.history_of_present_illness,
            "medical_history_summary": consultation.medical_history_summary,
            "dental_history_summary": consultation.dental_history_summary,
            "examination_summary": consultation.examination_summary,
            "provisional_diagnosis": consultation.provisional_diagnosis,
            "final_diagnosis": consultation.final_diagnosis,
            "notes": consultation.notes,
            "status": consultation.status,
            "is_active": consultation.is_active,
        }

        for field_name, old_val in old_values.items():
            new_val = new_values[field_name]
            if str(old_val) != str(new_val):
                AuditLogService.create_log(
                    model_name="Consultation",
                    record_id=consultation.uuid,
                    field_name=field_name,
                    old_value=old_val,
                    new_value=new_val,
                    user=user,
                )

        return consultation
