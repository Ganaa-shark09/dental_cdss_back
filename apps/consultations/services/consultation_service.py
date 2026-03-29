from datetime import date

from rest_framework.exceptions import ValidationError

from apps.appointments.models import Appointment
from apps.clinics.models import Clinic
from apps.consultations.models import Consultation
from apps.patients.models import Patient
from apps.staff.models import StaffProfile


class ConsultationService:
    @staticmethod
    def get_appointment(appointment_id):
        if not appointment_id:
            return None

        try:
            return Appointment.objects.select_related(
                "patient",
                "clinic",
                "staff_profile",
            ).get(id=appointment_id, is_active=True)
        except Appointment.DoesNotExist:
            raise ValidationError(
                {"appointment_id": ["Valid active appointment not found."]}
            )

    @staticmethod
    def get_patient(patient_id):
        try:
            return Patient.objects.get(id=patient_id, is_active=True)
        except Patient.DoesNotExist:
            raise ValidationError({"patient_id": ["Valid active patient not found."]})

    @staticmethod
    def get_clinic(clinic_id):
        try:
            return Clinic.objects.get(id=clinic_id, is_active=True)
        except Clinic.DoesNotExist:
            raise ValidationError({"clinic_id": ["Valid active clinic not found."]})

    @staticmethod
    def get_staff_profile(staff_profile_id):
        if not staff_profile_id:
            return None

        try:
            return StaffProfile.objects.select_related("clinic").get(
                id=staff_profile_id,
                is_active=True,
            )
        except StaffProfile.DoesNotExist:
            raise ValidationError(
                {"staff_profile_id": ["Valid active staff profile not found."]}
            )

    @staticmethod
    def validate_consultation_number_uniqueness(consultation_number: str):
        if Consultation.objects.filter(
            consultation_number__iexact=consultation_number
        ).exists():
            raise ValidationError(
                {
                    "consultation_number": [
                        "A consultation with this number already exists."
                    ]
                }
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
    def validate_appointment_not_already_linked(appointment):
        if (
            appointment
            and Consultation.objects.filter(appointment=appointment).exists()
        ):
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
    def create_consultation(cls, validated_data):
        appointment = cls.get_appointment(validated_data.get("appointment_id"))
        patient = cls.get_patient(validated_data["patient_id"])
        clinic = cls.get_clinic(validated_data["clinic_id"])
        staff_profile = cls.get_staff_profile(validated_data.get("staff_profile_id"))

        consultation_number = validated_data["consultation_number"].strip().upper()
        consultation_date = validated_data["consultation_date"]

        cls.validate_consultation_number_uniqueness(consultation_number)
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
            consultation_number=consultation_number,
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
    def get_consultation_by_id(consultation_id):
        try:
            return Consultation.objects.select_related(
                "appointment",
                "patient",
                "clinic",
                "staff_profile",
                "staff_profile__user",
            ).get(id=consultation_id)
        except Consultation.DoesNotExist:
            raise ValidationError({"consultation_id": ["Consultation not found."]})
