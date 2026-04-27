from rest_framework import serializers
from apps.cdss.models import CdssEngine


class CdssEngineSerializer(serializers.ModelSerializer):
    consultation = serializers.UUIDField(source="consultation.uuid", read_only=True)
    consultation_number = serializers.CharField(
        source="consultation.consultation_number", read_only=True
    )
    department_display = serializers.CharField(
        source="get_department_display", read_only=True
    )

    class Meta:
        model = CdssEngine
        fields = (
            "uuid",
            "consultation",
            "consultation_number",
            "department",
            "department_display",
            "risk_score",
            "alerts",
            "recommendations",
            "diagnosis_assistance",
            "icd_code",
            "confidence",
            "per_tooth_results",
            "is_active",
            "created_at",
            "updated_at",
        )


class CdssEngineUpdateSerializer(serializers.Serializer):
    department = serializers.ChoiceField(
        choices=[
            "GENERAL",
            "ENDODONTICS",
            "PERIODONTICS",
            "ORAL_SURGERY",
            "ORTHODONTICS",
            "PROSTHODONTICS",
            "PEDIATRIC",
            "PREVENTIVE",
        ],
        required=False,
    )
    risk_score = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False
    )
    alerts = serializers.ListField(child=serializers.CharField(), required=False)
    recommendations = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    diagnosis_assistance = serializers.CharField(required=False, allow_blank=True)
    icd_code = serializers.CharField(required=False, allow_blank=True)
    confidence = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)


class CdssEnginePrintSerializer(serializers.ModelSerializer):
    consultation_number = serializers.CharField(
        source="consultation.consultation_number", read_only=True
    )
    consultation_date = serializers.DateField(
        source="consultation.consultation_date", read_only=True
    )
    patient_name = serializers.CharField(
        source="consultation.patient.full_name", read_only=True
    )
    patient_code = serializers.CharField(
        source="consultation.patient.patient_code", read_only=True
    )
    patient_gender = serializers.CharField(
        source="consultation.patient.gender", read_only=True
    )
    patient_date_of_birth = serializers.DateField(
        source="consultation.patient.date_of_birth", read_only=True
    )
    clinic_name = serializers.CharField(
        source="consultation.clinic.name", read_only=True
    )
    clinic_address = serializers.CharField(
        source="consultation.clinic.address", read_only=True
    )
    doctor_name = serializers.SerializerMethodField()
    doctor_designation = serializers.SerializerMethodField()
    department_display = serializers.CharField(
        source="get_department_display", read_only=True
    )
    chief_complaint = serializers.CharField(
        source="consultation.chief_complaint", read_only=True
    )
    examination_summary = serializers.CharField(
        source="consultation.examination_summary", read_only=True
    )
    provisional_diagnosis = serializers.CharField(
        source="consultation.provisional_diagnosis", read_only=True
    )
    final_diagnosis = serializers.CharField(
        source="consultation.final_diagnosis", read_only=True
    )

    class Meta:
        model = CdssEngine
        fields = (
            "uuid",
            "consultation_number",
            "consultation_date",
            "patient_name",
            "patient_code",
            "patient_gender",
            "patient_date_of_birth",
            "clinic_name",
            "clinic_address",
            "doctor_name",
            "doctor_designation",
            "department",
            "department_display",
            "risk_score",
            "alerts",
            "recommendations",
            "diagnosis_assistance",
            "chief_complaint",
            "examination_summary",
            "provisional_diagnosis",
            "final_diagnosis",
            "created_at",
        )

    def get_doctor_name(self, obj):
        if obj.consultation.staff_profile:
            return obj.consultation.staff_profile.user.full_name
        return None

    def get_doctor_designation(self, obj):
        if obj.consultation.staff_profile:
            return obj.consultation.staff_profile.designation
        return None
