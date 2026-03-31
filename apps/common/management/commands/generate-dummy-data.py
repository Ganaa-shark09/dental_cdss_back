from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from apps.users.models import Role
from apps.clinics.models import Clinic
from apps.patients.models import Patient
from apps.staff.models import StaffProfile
from apps.appointments.models import Appointment
from apps.consultations.models import Consultation
from apps.prescriptions.models import Prescription
from apps.treatment_plans.models import TreatmentPlan
from apps.documents.models import Document
from apps.reports.models import Report
from apps.cdss.models import CdssEngine, CdssRecommendation
from apps.audit_logs.models import AuditLog
from apps.odontology.models import DentalChart, ToothRecord


class Command(BaseCommand):
    help = "Generate comprehensive dummy data for all apps"

    def handle(self, *args, **kwargs):
        self.generate_roles()
        self.generate_users()
        self.generate_clinics()
        self.generate_patients()
        self.generate_staff_profiles()
        self.generate_appointments()
        self.generate_consultations()
        self.generate_prescriptions()
        self.generate_treatment_plans()
        self.generate_documents()
        self.generate_reports()
        self.generate_cdss_data()
        self.generate_dental_charts()
        self.generate_tooth_records()
        self.generate_audit_logs()

        self.stdout.write(self.style.SUCCESS("Dummy data generation completed."))

    def generate_roles(self):
        roles = [
            {
                "name": "Super Admin",
                "code": "SUPER_ADMIN",
                "description": "System-wide super administrator",
            },
            {
                "name": "Clinic Admin",
                "code": "CLINIC_ADMIN",
                "description": "Clinic administrator",
            },
            {
                "name": "Dentist",
                "code": "DENTIST",
                "description": "Dental practitioner",
            },
            {
                "name": "Assistant",
                "code": "ASSISTANT",
                "description": "Dental assistant",
            },
            {
                "name": "Receptionist",
                "code": "RECEPTIONIST",
                "description": "Front desk staff",
            },
        ]

        for role_data in roles:
            role, created = Role.objects.get_or_create(
                code=role_data["code"],
                defaults={
                    "name": role_data["name"],
                    "description": role_data["description"],
                    "is_active": True,
                },
            )
            self.stdout.write(f"Role {role.name} {'created' if created else 'exists'}")

    def generate_users(self):
        users_data = [
            {
                "username": "admin",
                "email": "admin@dentalcdss.com",
                "password": "password123",
                "first_name": "System",
                "last_name": "Admin",
                "phone_number": "9999999991",
                "role_code": "SUPER_ADMIN",
                "is_staff": True,
                "is_active": True,
            },
            {
                "username": "clinicadmin",
                "email": "clinicadmin@dentalcdss.com",
                "password": "password123",
                "first_name": "Clinic",
                "last_name": "Admin",
                "phone_number": "9999999992",
                "role_code": "CLINIC_ADMIN",
                "is_staff": True,
                "is_active": True,
            },
            {
                "username": "dentist",
                "email": "dentist@dentalcdss.com",
                "password": "password123",
                "first_name": "Arjun",
                "last_name": "Dentist",
                "phone_number": "9999999993",
                "role_code": "DENTIST",
                "is_staff": True,
                "is_active": True,
            },
            {
                "username": "assistant",
                "email": "assistant@dentalcdss.com",
                "password": "password123",
                "first_name": "Maya",
                "last_name": "Assistant",
                "phone_number": "9999999994",
                "role_code": "ASSISTANT",
                "is_staff": True,
                "is_active": True,
            },
            {
                "username": "receptionist",
                "email": "receptionist@dentalcdss.com",
                "password": "password123",
                "first_name": "Neha",
                "last_name": "Reception",
                "phone_number": "9999999995",
                "role_code": "RECEPTIONIST",
                "is_staff": True,
                "is_active": True,
            },
        ]

        roles = {role.code: role for role in Role.objects.all()}
        User = get_user_model()

        for user_data in users_data:
            user = User.objects.filter(username=user_data["username"]).first()

            if not user:
                user = User.objects.filter(email=user_data["email"]).first()

            if not user:
                user = User.objects.create_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    phone_number=user_data["phone_number"],
                    is_staff=user_data["is_staff"],
                    is_active=user_data["is_active"],
                    role=roles.get(user_data["role_code"]),
                )
                self.stdout.write(
                    f"User {user.username} created and role {user.role.name if user.role else 'None'} assigned."
                )
            else:
                changed = False

                if not user.username:
                    user.username = user_data["username"]
                    changed = True
                if not user.email:
                    user.email = user_data["email"]
                    changed = True
                if not user.first_name:
                    user.first_name = user_data["first_name"]
                    changed = True
                if not user.last_name:
                    user.last_name = user_data["last_name"]
                    changed = True
                if not user.phone_number:
                    user.phone_number = user_data["phone_number"]
                    changed = True
                if user.role is None:
                    user.role = roles.get(user_data["role_code"])
                    changed = True

                if changed:
                    user.save()

                self.stdout.write(
                    f"User {user.username or user.email} already exists, reused."
                )

    def generate_clinics(self):
        clinics_data = [
            {
                "code": "CLINIC_A",
                "name": "Dental Clinic A",
                "email": "clinicA@dental.com",
                "phone_number": "+1234567890",
                "address": "123 Dental St.",
                "city": "Dentown",
                "state": "Dentalstate",
                "country": "Dentland",
                "postal_code": "12345",
                "is_active": True,
            },
            {
                "code": "CLINIC_B",
                "name": "Dental Clinic B",
                "email": "clinicB@dental.com",
                "phone_number": "+0987654321",
                "address": "456 Dental Ave.",
                "city": "Medcity",
                "state": "Healthstate",
                "country": "Medland",
                "postal_code": "54321",
                "is_active": True,
            },
        ]

        for clinic_data in clinics_data:
            clinic, created = Clinic.objects.get_or_create(
                code=clinic_data["code"],
                defaults=clinic_data,
            )
            self.stdout.write(
                f"Clinic {clinic.name} {'created' if created else 'already exists'}."
            )

    def generate_patients(self):
        patients_data = [
            {
                "patient_code": "P001",
                "first_name": "John",
                "last_name": "Doe",
                "gender": "MALE",
                "date_of_birth": "1990-01-01",
                "phone_number": "8888888881",
                "email": "john.doe@example.com",
                "address": "12 Main Street",
                "city": "Dentown",
                "state": "Dentalstate",
                "country": "Dentland",
                "postal_code": "400001",
                "blood_group": "O+",
                "marital_status": "Single",
                "occupation": "Engineer",
                "emergency_contact_name": "Jake Doe",
                "emergency_contact_phone": "7777777771",
                "is_active": True,
            },
            {
                "patient_code": "P002",
                "first_name": "Jane",
                "last_name": "Smith",
                "gender": "FEMALE",
                "date_of_birth": "1985-02-15",
                "phone_number": "8888888882",
                "email": "jane.smith@example.com",
                "address": "45 Park Avenue",
                "city": "Dentown",
                "state": "Dentalstate",
                "country": "Dentland",
                "postal_code": "400002",
                "blood_group": "A+",
                "marital_status": "Married",
                "occupation": "Teacher",
                "emergency_contact_name": "Sam Smith",
                "emergency_contact_phone": "7777777772",
                "is_active": True,
            },
        ]

        for patient_data in patients_data:
            patient, created = Patient.objects.get_or_create(
                patient_code=patient_data["patient_code"],
                defaults=patient_data,
            )
            self.stdout.write(
                f"Patient {patient.full_name} {'created' if created else 'already exists'}."
            )

    def generate_staff_profiles(self):
        staff_profiles_data = [
            {
                "username": "clinicadmin",
                "clinic_code": "CLINIC_A",
                "employee_id": "EMP001",
                "designation": "Clinic Administrator",
                "specialization": "",
                "license_number": "",
                "years_of_experience": 7,
                "is_active": True,
            },
            {
                "username": "dentist",
                "clinic_code": "CLINIC_A",
                "employee_id": "EMP002",
                "designation": "Dentist",
                "specialization": "Endodontics",
                "license_number": "DEN-LIC-001",
                "years_of_experience": 10,
                "is_active": True,
            },
            {
                "username": "assistant",
                "clinic_code": "CLINIC_A",
                "employee_id": "EMP003",
                "designation": "Dental Assistant",
                "specialization": "",
                "license_number": "",
                "years_of_experience": 4,
                "is_active": True,
            },
            {
                "username": "receptionist",
                "clinic_code": "CLINIC_A",
                "employee_id": "EMP004",
                "designation": "Receptionist",
                "specialization": "",
                "license_number": "",
                "years_of_experience": 3,
                "is_active": True,
            },
        ]

        User = get_user_model()

        for data in staff_profiles_data:
            user = User.objects.get(username=data["username"])
            clinic = Clinic.objects.get(code=data["clinic_code"])

            staff_profile, created = StaffProfile.objects.get_or_create(
                user=user,
                defaults={
                    "clinic": clinic,
                    "employee_id": data["employee_id"],
                    "designation": data["designation"],
                    "specialization": data["specialization"],
                    "license_number": data["license_number"],
                    "years_of_experience": data["years_of_experience"],
                    "is_active": data["is_active"],
                },
            )
            self.stdout.write(
                f"StaffProfile for {user.username} {'created' if created else 'already exists'}."
            )

    def generate_appointments(self):
        appointments_data = [
            {
                "patient_code": "P001",
                "clinic_code": "CLINIC_A",
                "staff_username": "dentist",
                "appointment_number": "APPT001",
                "appointment_date": "2023-06-01",
                "appointment_time": "09:00:00",
                "status": "SCHEDULED",
                "reason_for_visit": "Tooth pain",
                "notes": "First visit",
                "is_active": True,
            },
            {
                "patient_code": "P002",
                "clinic_code": "CLINIC_A",
                "staff_username": "dentist",
                "appointment_number": "APPT002",
                "appointment_date": "2023-06-02",
                "appointment_time": "10:00:00",
                "status": "CONFIRMED",
                "reason_for_visit": "Routine check-up",
                "notes": "Returning patient",
                "is_active": True,
            },
        ]

        for data in appointments_data:
            patient = Patient.objects.get(patient_code=data["patient_code"])
            clinic = Clinic.objects.get(code=data["clinic_code"])
            staff_profile = StaffProfile.objects.filter(
                user__username=data["staff_username"]
            ).first()

            appointment, created = Appointment.objects.get_or_create(
                appointment_number=data["appointment_number"],
                defaults={
                    "patient": patient,
                    "clinic": clinic,
                    "staff_profile": staff_profile,
                    "appointment_date": data["appointment_date"],
                    "appointment_time": data["appointment_time"],
                    "status": data["status"],
                    "reason_for_visit": data["reason_for_visit"],
                    "notes": data["notes"],
                    "is_active": data["is_active"],
                },
            )
            self.stdout.write(
                f"Appointment {appointment.appointment_number} {'created' if created else 'already exists'}."
            )

    def generate_consultations(self):
        consultations_data = [
            {
                "appointment_number": "APPT001",
                "patient_code": "P001",
                "clinic_code": "CLINIC_A",
                "staff_username": "dentist",
                "consultation_number": "CONSULT001",
                "consultation_date": "2023-06-01",
                "consultation_time": "09:30:00",
                "chief_complaint": "Severe toothache on lower right molar",
                "history_of_present_illness": "Pain for 3 days, worse at night",
                "medical_history_summary": "No diabetes, no hypertension",
                "dental_history_summary": "Previous filling 2 years ago",
                "examination_summary": "Deep caries on tooth 46",
                "provisional_diagnosis": "Irreversible pulpitis",
                "final_diagnosis": "Irreversible pulpitis with apical periodontitis",
                "notes": "Root canal advised",
                "status": "IN_PROGRESS",
                "is_active": True,
            },
            {
                "appointment_number": "APPT002",
                "patient_code": "P002",
                "clinic_code": "CLINIC_A",
                "staff_username": "dentist",
                "consultation_number": "CONSULT002",
                "consultation_date": "2023-06-02",
                "consultation_time": "10:30:00",
                "chief_complaint": "Routine dental cleaning",
                "history_of_present_illness": "No active pain",
                "medical_history_summary": "Fit and healthy",
                "dental_history_summary": "Regular cleanings",
                "examination_summary": "Mild plaque and calculus",
                "provisional_diagnosis": "Chronic generalized gingivitis",
                "final_diagnosis": "Mild chronic generalized gingivitis",
                "notes": "Scaling recommended",
                "status": "COMPLETED",
                "is_active": True,
            },
        ]

        for data in consultations_data:
            appointment = Appointment.objects.get(
                appointment_number=data["appointment_number"]
            )
            patient = Patient.objects.get(patient_code=data["patient_code"])
            clinic = Clinic.objects.get(code=data["clinic_code"])
            staff_profile = StaffProfile.objects.filter(
                user__username=data["staff_username"]
            ).first()

            consultation, created = Consultation.objects.get_or_create(
                consultation_number=data["consultation_number"],
                defaults={
                    "appointment": appointment,
                    "patient": patient,
                    "clinic": clinic,
                    "staff_profile": staff_profile,
                    "consultation_date": data["consultation_date"],
                    "consultation_time": data["consultation_time"],
                    "chief_complaint": data["chief_complaint"],
                    "history_of_present_illness": data["history_of_present_illness"],
                    "medical_history_summary": data["medical_history_summary"],
                    "dental_history_summary": data["dental_history_summary"],
                    "examination_summary": data["examination_summary"],
                    "provisional_diagnosis": data["provisional_diagnosis"],
                    "final_diagnosis": data["final_diagnosis"],
                    "notes": data["notes"],
                    "status": data["status"],
                    "is_active": data["is_active"],
                },
            )
            self.stdout.write(
                f"Consultation {consultation.consultation_number} {'created' if created else 'already exists'}."
            )

    def generate_prescriptions(self):
        prescriptions_data = [
            {
                "consultation_number": "CONSULT001",
                "patient_code": "P001",
                "medication": "Paracetamol",
                "dosage": "500mg",
                "treatment_instructions": "Take once every 6 hours after food for 3 days",
                "notes": "Pain control",
                "date_issued": "2023-06-01",
                "expiry_date": "2023-06-07",
                "is_active": True,
            },
            {
                "consultation_number": "CONSULT002",
                "patient_code": "P002",
                "medication": "Chlorhexidine Mouthwash",
                "dosage": "10ml",
                "treatment_instructions": "Rinse twice daily for 7 days",
                "notes": "Post scaling care",
                "date_issued": "2023-06-02",
                "expiry_date": "2023-06-09",
                "is_active": True,
            },
        ]

        for data in prescriptions_data:
            consultation = Consultation.objects.get(
                consultation_number=data["consultation_number"]
            )
            patient = Patient.objects.get(patient_code=data["patient_code"])

            prescription = (
                Prescription.objects.filter(
                    consultation=consultation,
                    patient=patient,
                    medication=data["medication"],
                )
                .order_by("id")
                .first()
            )

            if prescription:
                self.stdout.write(
                    f"Prescription for {patient.full_name} already exists, reused."
                )
                continue

            prescription = Prescription.objects.create(
                consultation=consultation,
                patient=patient,
                medication=data["medication"],
                dosage=data["dosage"],
                treatment_instructions=data["treatment_instructions"],
                notes=data["notes"],
                date_issued=data["date_issued"],
                expiry_date=data["expiry_date"],
                is_active=data["is_active"],
            )
            self.stdout.write(f"Prescription for {patient.full_name} created.")

    def generate_treatment_plans(self):
        treatment_plans_data = [
            {
                "consultation_number": "CONSULT001",
                "treatment_type": "Root Canal",
                "treatment_description": "RCT for tooth 46 followed by crown placement",
                "start_date": "2023-06-03",
                "end_date": "2023-06-10",
                "status": "PLANNED",
                "is_active": True,
            },
            {
                "consultation_number": "CONSULT002",
                "treatment_type": "Scaling",
                "treatment_description": "Full mouth ultrasonic scaling and polishing",
                "start_date": "2023-06-02",
                "end_date": "2023-06-02",
                "status": "COMPLETED",
                "is_active": True,
            },
        ]

        for data in treatment_plans_data:
            consultation = Consultation.objects.get(
                consultation_number=data["consultation_number"]
            )

            treatment_plan = (
                TreatmentPlan.objects.filter(
                    consultation=consultation,
                    treatment_type=data["treatment_type"],
                )
                .order_by("id")
                .first()
            )

            if treatment_plan:
                self.stdout.write(
                    f"Treatment Plan for {consultation.consultation_number} already exists, reused."
                )
                continue

            treatment_plan = TreatmentPlan.objects.create(
                consultation=consultation,
                treatment_type=data["treatment_type"],
                treatment_description=data["treatment_description"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                status=data["status"],
                is_active=data["is_active"],
            )
            self.stdout.write(
                f"Treatment Plan for {consultation.consultation_number} created."
            )

    def generate_documents(self):
        documents_data = [
            {
                "consultation_number": "CONSULT001",
                "document_type": "X-ray",
                "file_path": "documents/xray_001.jpg",
                "description": "IOPA X-ray for tooth 46",
                "is_active": True,
            },
            {
                "consultation_number": "CONSULT002",
                "document_type": "Prescription",
                "file_path": "documents/prescription_002.pdf",
                "description": "Prescription and post-treatment instructions",
                "is_active": True,
            },
        ]

        for data in documents_data:
            consultation = Consultation.objects.get(
                consultation_number=data["consultation_number"]
            )

            document = (
                Document.objects.filter(
                    consultation=consultation,
                    document_type=data["document_type"],
                )
                .order_by("id")
                .first()
            )

            if document:
                self.stdout.write(
                    f"Document for {consultation.consultation_number} already exists, reused."
                )
                continue

            document = Document.objects.create(
                consultation=consultation,
                document_type=data["document_type"],
                document=data["file_path"],
                description=data["description"],
                is_active=data["is_active"],
            )
            self.stdout.write(
                f"Document for {consultation.consultation_number} created."
            )

    def generate_reports(self):
        reports_data = [
            {
                "consultation_number": "CONSULT001",
                "report_type": "Consultation Summary",
                "notes": "Patient requires urgent endodontic treatment.",
                "is_active": True,
            },
            {
                "consultation_number": "CONSULT002",
                "report_type": "Treatment Completion Report",
                "notes": "Scaling completed successfully. Oral hygiene instructions given.",
                "is_active": True,
            },
        ]

        for data in reports_data:
            consultation = Consultation.objects.get(
                consultation_number=data["consultation_number"]
            )
            prescription = (
                Prescription.objects.filter(consultation=consultation)
                .order_by("id")
                .first()
            )
            treatment_plan = (
                TreatmentPlan.objects.filter(consultation=consultation)
                .order_by("id")
                .first()
            )

            report = (
                Report.objects.filter(
                    consultation=consultation,
                    report_type=data["report_type"],
                )
                .order_by("id")
                .first()
            )

            if report:
                self.stdout.write(
                    f"Report for {consultation.consultation_number} already exists, reused."
                )
                continue

            report = Report.objects.create(
                consultation=consultation,
                report_type=data["report_type"],
                prescription_summary=prescription,
                treatment_plan_summary=treatment_plan,
                notes=data["notes"],
                is_active=data["is_active"],
            )
            self.stdout.write(f"Report for {consultation.consultation_number} created.")

    def generate_cdss_data(self):
        cdss_data = [
            {
                "consultation_number": "CONSULT001",
                "risk_score": 4.5,
                "alerts": ["Possible pulpal involvement", "Pain severity high"],
                "recommendations": [
                    "Root canal treatment",
                    "Pain management",
                    "Radiographic evaluation",
                ],
                "diagnosis_assistance": "Clinical signs are consistent with irreversible pulpitis.",
                "recommendation_text": "Initiate endodontic management for tooth 46.",
                "is_active": True,
            },
            {
                "consultation_number": "CONSULT002",
                "risk_score": 2.0,
                "alerts": ["Plaque accumulation"],
                "recommendations": ["Scaling", "Oral hygiene reinforcement"],
                "diagnosis_assistance": "Findings suggest mild chronic gingivitis.",
                "recommendation_text": "Schedule regular scaling and reinforce brushing technique.",
                "is_active": True,
            },
        ]

        for data in cdss_data:
            consultation = Consultation.objects.get(
                consultation_number=data["consultation_number"]
            )

            cdss_engine = CdssEngine.objects.filter(consultation=consultation).first()

            if not cdss_engine:
                cdss_engine = CdssEngine.objects.create(
                    consultation=consultation,
                    risk_score=data["risk_score"],
                    alerts=data["alerts"],
                    recommendations=data["recommendations"],
                    diagnosis_assistance=data["diagnosis_assistance"],
                    is_active=data["is_active"],
                )
                self.stdout.write(
                    f"CDSS Engine for {consultation.consultation_number} created."
                )
            else:
                self.stdout.write(
                    f"CDSS Engine for {consultation.consultation_number} already exists, reused."
                )

            recommendation = (
                CdssRecommendation.objects.filter(
                    cdss_engine=cdss_engine,
                    recommendation=data["recommendation_text"],
                )
                .order_by("id")
                .first()
            )

            if recommendation:
                self.stdout.write(
                    f"Recommendation for {consultation.consultation_number} already exists, reused."
                )
                continue

            CdssRecommendation.objects.create(
                cdss_engine=cdss_engine,
                recommendation=data["recommendation_text"],
                is_active=True,
            )
            self.stdout.write(
                f"Recommendation for {consultation.consultation_number} created."
            )

    def generate_dental_charts(self):
        charts_data = [
            {
                "consultation_number": "CONSULT001",
                "notes": "Dental chart created for endodontic evaluation.",
                "is_active": True,
            },
            {
                "consultation_number": "CONSULT002",
                "notes": "Dental chart created for routine examination.",
                "is_active": True,
            },
        ]

        for data in charts_data:
            consultation = Consultation.objects.get(
                consultation_number=data["consultation_number"]
            )

            chart, created = DentalChart.objects.get_or_create(
                consultation=consultation,
                defaults={
                    "notes": data["notes"],
                    "is_active": data["is_active"],
                },
            )
            self.stdout.write(
                f"DentalChart for {consultation.consultation_number} {'created' if created else 'already exists'}."
            )

    def generate_tooth_records(self):
        tooth_records_data = [
            {
                "consultation_number": "CONSULT001",
                "tooth_number": "46",
                "condition": "CARIES",
                "surfaces": ["OCCLUSAL", "DISTAL"],
                "mobility_grade": None,
                "percussion_tenderness": True,
                "palpation_tenderness": False,
                "probing_depth_summary": "3-4 mm",
                "notes": "Deep carious lesion with tenderness.",
                "is_active": True,
            },
            {
                "consultation_number": "CONSULT002",
                "tooth_number": "11",
                "condition": "SOUND",
                "surfaces": [],
                "mobility_grade": None,
                "percussion_tenderness": False,
                "palpation_tenderness": False,
                "probing_depth_summary": "1-2 mm",
                "notes": "Healthy tooth.",
                "is_active": True,
            },
            {
                "consultation_number": "CONSULT002",
                "tooth_number": "16",
                "condition": "FILLED",
                "surfaces": ["OCCLUSAL"],
                "mobility_grade": None,
                "percussion_tenderness": False,
                "palpation_tenderness": False,
                "probing_depth_summary": "2 mm",
                "notes": "Existing restoration intact.",
                "is_active": True,
            },
        ]

        for data in tooth_records_data:
            consultation = Consultation.objects.get(
                consultation_number=data["consultation_number"]
            )
            chart = DentalChart.objects.get(consultation=consultation)

            tooth_record, created = ToothRecord.objects.get_or_create(
                chart=chart,
                tooth_number=data["tooth_number"],
                defaults={
                    "condition": data["condition"],
                    "surfaces": data["surfaces"],
                    "mobility_grade": data["mobility_grade"],
                    "percussion_tenderness": data["percussion_tenderness"],
                    "palpation_tenderness": data["palpation_tenderness"],
                    "probing_depth_summary": data["probing_depth_summary"],
                    "notes": data["notes"],
                    "is_active": data["is_active"],
                },
            )
            self.stdout.write(
                f"ToothRecord {tooth_record.tooth_number} for {consultation.consultation_number} {'created' if created else 'already exists'}."
            )

    def generate_audit_logs(self):
        audit_logs_data = [
            {
                "model_name": "Patient",
                "record_lookup": {"patient_code": "P001"},
                "field_name": "phone_number",
                "old_value": "8888888800",
                "new_value": "8888888881",
                "username": "clinicadmin",
            },
            {
                "model_name": "Appointment",
                "record_lookup": {"appointment_number": "APPT001"},
                "field_name": "status",
                "old_value": "SCHEDULED",
                "new_value": "CONFIRMED",
                "username": "receptionist",
            },
            {
                "model_name": "Consultation",
                "record_lookup": {"consultation_number": "CONSULT001"},
                "field_name": "final_diagnosis",
                "old_value": "Irreversible pulpitis",
                "new_value": "Irreversible pulpitis with apical periodontitis",
                "username": "dentist",
            },
        ]

        User = get_user_model()

        model_map = {
            "Patient": Patient,
            "Appointment": Appointment,
            "Consultation": Consultation,
            "DentalChart": DentalChart,
            "ToothRecord": ToothRecord,
        }

        for data in audit_logs_data:
            model_class = model_map[data["model_name"]]
            record = model_class.objects.filter(**data["record_lookup"]).first()
            user = User.objects.get(username=data["username"])

            if not record:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipped AuditLog for {data['model_name']} because record was not found."
                    )
                )
                continue

            audit_log, created = AuditLog.objects.get_or_create(
                model_name=data["model_name"],
                record_id=record.uuid,
                field_name=data["field_name"],
                user=user,
                defaults={
                    "old_value": data["old_value"],
                    "new_value": data["new_value"],
                },
            )
            self.stdout.write(
                f"AuditLog for {data['model_name']} ({data['field_name']}) {'created' if created else 'already exists'}."
            )
