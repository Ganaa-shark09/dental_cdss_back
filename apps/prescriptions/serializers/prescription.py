from rest_framework import serializers
from apps.prescriptions.models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    consultation = serializers.UUIDField(source="consultation.uuid", read_only=True)
    consultation_number = serializers.CharField(
        source="consultation.consultation_number", read_only=True
    )
    patient = serializers.UUIDField(source="patient.uuid", read_only=True)
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)

    class Meta:
        model = Prescription
        fields = (
            "uuid",
            "consultation",
            "consultation_number",
            "patient",
            "patient_name",
            "medication",
            "dosage",
            "treatment_instructions",
            "notes",
            "date_issued",
            "expiry_date",
            "is_active",
            "created_at",
            "updated_at",
        )


class PrescriptionCreateSerializer(serializers.Serializer):
    consultation_id = serializers.UUIDField()
    patient_id = serializers.UUIDField()
    medication = serializers.CharField(max_length=255)
    dosage = serializers.CharField(max_length=255)
    treatment_instructions = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)
    date_issued = serializers.DateField()
    expiry_date = serializers.DateField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False, default=True)


class PrescriptionUpdateSerializer(serializers.Serializer):
    consultation_id = serializers.UUIDField(required=False)
    patient_id = serializers.UUIDField(required=False)
    medication = serializers.CharField(max_length=255, required=False)
    dosage = serializers.CharField(max_length=255, required=False)
    treatment_instructions = serializers.CharField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    date_issued = serializers.DateField(required=False)
    expiry_date = serializers.DateField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)


class PrescriptionPrintSerializer(serializers.ModelSerializer):
    consultation_number = serializers.CharField(
        source="consultation.consultation_number", read_only=True
    )
    consultation_date = serializers.DateField(
        source="consultation.consultation_date", read_only=True
    )
    consultation_time = serializers.TimeField(
        source="consultation.consultation_time", read_only=True
    )
    chief_complaint = serializers.CharField(
        source="consultation.chief_complaint", read_only=True
    )
    provisional_diagnosis = serializers.CharField(
        source="consultation.provisional_diagnosis", read_only=True
    )
    final_diagnosis = serializers.CharField(
        source="consultation.final_diagnosis", read_only=True
    )
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    patient_code = serializers.CharField(source="patient.patient_code", read_only=True)
    patient_gender = serializers.CharField(source="patient.gender", read_only=True)
    patient_date_of_birth = serializers.DateField(
        source="patient.date_of_birth", read_only=True
    )
    patient_phone = serializers.CharField(
        source="patient.phone_number", read_only=True
    )
    clinic_name = serializers.CharField(
        source="consultation.clinic.name", read_only=True
    )
    clinic_address = serializers.CharField(
        source="consultation.clinic.address", read_only=True
    )
    clinic_phone = serializers.CharField(
        source="consultation.clinic.phone_number", read_only=True
    )
    doctor_name = serializers.SerializerMethodField()
    doctor_designation = serializers.SerializerMethodField()
    doctor_license = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = (
            "uuid",
            "consultation_number",
            "consultation_date",
            "consultation_time",
            "chief_complaint",
            "provisional_diagnosis",
            "final_diagnosis",
            "patient_name",
            "patient_code",
            "patient_gender",
            "patient_date_of_birth",
            "patient_phone",
            "clinic_name",
            "clinic_address",
            "clinic_phone",
            "doctor_name",
            "doctor_designation",
            "doctor_license",
            "medication",
            "dosage",
            "treatment_instructions",
            "notes",
            "date_issued",
            "expiry_date",
        )

    def get_doctor_name(self, obj):
        if obj.consultation.staff_profile:
            return obj.consultation.staff_profile.user.full_name
        return None

    def get_doctor_designation(self, obj):
        if obj.consultation.staff_profile:
            return obj.consultation.staff_profile.designation
        return None

    def get_doctor_license(self, obj):
        if obj.consultation.staff_profile:
            return obj.consultation.staff_profile.license_number
        return None
