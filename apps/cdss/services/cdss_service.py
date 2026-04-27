from decimal import Decimal
from datetime import date

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.consultations.models import Consultation
from apps.cdss.models import CdssEngine, CdssRecommendation
from apps.cdss.engines.universal_brain import run_universal_brain


class CdssService:

    # ── Department keyword maps ─────────────────────────────────────────────
    ENDODONTIC_KEYWORDS = [
        "root canal", "pulpitis", "pulp", "periapical", "abscess",
        "toothache", "tooth ache", "tooth pain", "dental pulp",
        "irreversible pulpitis", "reversible pulpitis", "necrotic",
    ]
    PERIODONTIC_KEYWORDS = [
        "gum", "gums", "periodontal", "gingivitis", "periodontitis",
        "bleeding gum", "loose tooth", "loose teeth", "mobility",
        "bone loss", "gingival", "plaque", "calculus", "tartar",
        "pocket depth", "furcation",
    ]
    ORAL_SURGERY_KEYWORDS = [
        "extraction", "impacted", "wisdom tooth", "wisdom teeth",
        "swelling", "cellulitis", "fracture", "jaw pain",
        "tmj", "temporomandibular", "cyst", "tumor", "lesion",
        "biopsy", "alveolar", "trismus", "facial swelling",
    ]
    ORTHODONTIC_KEYWORDS = [
        "crowding", "spacing", "crossbite", "overbite", "underbite",
        "malocclusion", "misalignment", "braces", "alignment",
        "open bite", "deep bite", "midline shift",
    ]
    PROSTHODONTIC_KEYWORDS = [
        "missing tooth", "missing teeth", "edentulous", "denture",
        "crown", "bridge", "implant", "prosthesis", "restoration",
        "veneer", "inlay", "onlay", "partial denture",
    ]
    PREVENTIVE_KEYWORDS = [
        "check up", "checkup", "routine", "cleaning", "prophylaxis",
        "fluoride", "sealant", "prevention", "no complaint",
        "no pain", "routine visit",
    ]

    # ── Risk weight per tooth condition ─────────────────────────────────────
    TOOTH_CONDITION_RISK = {
        "CARIES": 3,
        "FRACTURED": 4,
        "MOBILE": 5,
        "ROOT_STUMP": 6,
        "IMPACTED": 4,
        "MISSING": 2,
        "FILLED": 1,
        "ABFRACTION": 2,
        "ABRASION": 2,
        "ATTRITION": 2,
        "DISCOLORED": 1,
        "SOUND": 0,
    }

    # ── Department recommendations map ──────────────────────────────────────
    DEPT_RECOMMENDATIONS = {
        CdssEngine.DEPT_ENDODONTICS: [
            "Refer to Endodontics department for root canal evaluation.",
            "Take periapical X-ray to assess pulp and periapical status.",
            "Consider prescribing analgesics (Ibuprofen 400 mg TID) for pain management.",
        ],
        CdssEngine.DEPT_PERIODONTICS: [
            "Refer to Periodontics department for full periodontal evaluation.",
            "Perform scaling and root planing (SRP) if indicated.",
            "Advise improved oral hygiene: brushing twice daily and flossing.",
            "Schedule 3-month periodontal maintenance recall.",
        ],
        CdssEngine.DEPT_ORAL_SURGERY: [
            "Refer to Oral Surgery department for surgical evaluation.",
            "Take OPG/CBCT radiograph for proper surgical planning.",
            "Evaluate need for antibiotic prophylaxis prior to procedure.",
        ],
        CdssEngine.DEPT_ORTHODONTICS: [
            "Refer to Orthodontics department for malocclusion assessment.",
            "Take full orthodontic records: clinical photos, X-rays, and study models.",
            "Evaluate skeletal vs. dental component of malocclusion.",
        ],
        CdssEngine.DEPT_PROSTHODONTICS: [
            "Refer to Prosthodontics for restorative evaluation.",
            "Assess occlusal vertical dimension and existing prosthesis condition.",
            "Evaluate options: implant, bridge, or removable partial denture.",
        ],
        CdssEngine.DEPT_PEDIATRIC: [
            "Refer to Pediatric Dentistry for age-appropriate evaluation.",
            "Apply fluoride varnish and provide dietary counseling.",
            "Consider stainless steel crowns or pulpotomy for primary teeth.",
        ],
        CdssEngine.DEPT_PREVENTIVE: [
            "Schedule professional cleaning and prophylaxis.",
            "Apply fluoride varnish and provide oral hygiene instructions.",
            "Consider fissure sealants for caries prevention.",
        ],
        CdssEngine.DEPT_GENERAL: [
            "Proceed with comprehensive clinical evaluation and treatment planning.",
            "Take baseline periapical and bitewing radiographs if not done.",
        ],
    }

    # ────────────────────────────────────────────────────────────────────────
    # Helpers
    # ────────────────────────────────────────────────────────────────────────

    @staticmethod
    def get_consultation(consultation_uuid):
        try:
            return Consultation.objects.select_related(
                "patient", "clinic", "staff_profile", "staff_profile__user"
            ).get(uuid=consultation_uuid, is_active=True)
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid consultation not found."]}
            )

    @staticmethod
    def get_cdss_engine_by_uuid(cdss_engine_uuid):
        try:
            return CdssEngine.objects.select_related(
                "consultation",
                "consultation__patient",
                "consultation__clinic",
                "consultation__staff_profile",
                "consultation__staff_profile__user",
            ).get(uuid=cdss_engine_uuid)
        except CdssEngine.DoesNotExist:
            raise ValidationError({"cdss_engine_uuid": ["CDSS engine not found."]})

    @staticmethod
    def list_cdss_engines():
        return (
            CdssEngine.objects.select_related("consultation")
            .all()
            .order_by("-created_at")
        )

    @staticmethod
    def list_cdss_recommendations(cdss_engine_uuid):
        cdss_engine = CdssService.get_cdss_engine_by_uuid(cdss_engine_uuid)
        return cdss_engine.cdss_recommendations.all().order_by("-created_at")

    @staticmethod
    def _safe_lower(value):
        return (value or "").lower()

    @classmethod
    def _get_tooth_records(cls, consultation):
        try:
            dental_chart = consultation.dental_chart
            return list(dental_chart.tooth_records.filter(is_active=True))
        except Exception:
            return []

    # ────────────────────────────────────────────────────────────────────────
    # Department detection
    # ────────────────────────────────────────────────────────────────────────

    @classmethod
    def determine_department(cls, consultation):
        text = " ".join([
            cls._safe_lower(consultation.chief_complaint),
            cls._safe_lower(consultation.history_of_present_illness),
            cls._safe_lower(consultation.dental_history_summary),
            cls._safe_lower(consultation.examination_summary),
        ])

        tooth_records = cls._get_tooth_records(consultation)
        conditions = {r.condition for r in tooth_records}

        # Oral Surgery (highest priority — acute/surgical)
        if any(kw in text for kw in cls.ORAL_SURGERY_KEYWORDS) or \
                conditions & {"IMPACTED", "FRACTURED"}:
            return CdssEngine.DEPT_ORAL_SURGERY

        # Endodontics
        if any(kw in text for kw in cls.ENDODONTIC_KEYWORDS) or \
                conditions & {"CARIES", "ROOT_STUMP"}:
            return CdssEngine.DEPT_ENDODONTICS

        # Periodontics
        if any(kw in text for kw in cls.PERIODONTIC_KEYWORDS) or \
                conditions & {"MOBILE"}:
            return CdssEngine.DEPT_PERIODONTICS

        # Prosthodontics
        if any(kw in text for kw in cls.PROSTHODONTIC_KEYWORDS) or \
                conditions & {"MISSING"}:
            return CdssEngine.DEPT_PROSTHODONTICS

        # Orthodontics
        if any(kw in text for kw in cls.ORTHODONTIC_KEYWORDS):
            return CdssEngine.DEPT_ORTHODONTICS

        # Preventive
        if any(kw in text for kw in cls.PREVENTIVE_KEYWORDS):
            return CdssEngine.DEPT_PREVENTIVE

        return CdssEngine.DEPT_GENERAL

    # ────────────────────────────────────────────────────────────────────────
    # Risk scoring
    # ────────────────────────────────────────────────────────────────────────

    @classmethod
    def calculate_risk_score(cls, consultation):
        risk_score = Decimal("0.00")

        chief_complaint = cls._safe_lower(consultation.chief_complaint)
        medical_history = cls._safe_lower(consultation.medical_history_summary)

        if "pain" in chief_complaint:
            risk_score += Decimal("5.00")
        if "severe" in chief_complaint:
            risk_score += Decimal("3.00")
        if "swelling" in chief_complaint:
            risk_score += Decimal("4.00")
        if "bleeding" in chief_complaint:
            risk_score += Decimal("3.00")
        if "infection" in medical_history:
            risk_score += Decimal("3.00")
        if "diabetes" in medical_history:
            risk_score += Decimal("2.00")
        if "hypertension" in medical_history or "blood pressure" in medical_history:
            risk_score += Decimal("1.00")
        if "anticoagulant" in medical_history or "blood thinner" in medical_history:
            risk_score += Decimal("3.00")

        # Add risk from tooth conditions recorded in the dental chart
        tooth_records = cls._get_tooth_records(consultation)
        for record in tooth_records:
            condition_risk = cls.TOOTH_CONDITION_RISK.get(record.condition, 0)
            risk_score += Decimal(str(condition_risk))

        return min(risk_score, Decimal("100.00"))

    # ────────────────────────────────────────────────────────────────────────
    # Alert generation
    # ────────────────────────────────────────────────────────────────────────

    @classmethod
    def generate_alerts(cls, consultation):
        alerts = []

        medical_history = cls._safe_lower(consultation.medical_history_summary)
        chief_complaint = cls._safe_lower(consultation.chief_complaint)

        if "infection" in medical_history:
            alerts.append("Risk of infection due to existing conditions.")
        if "diabetes" in medical_history:
            alerts.append(
                "Patient has diabetes — monitor healing and consider antibiotic prophylaxis."
            )
        if "anticoagulant" in medical_history or "blood thinner" in medical_history:
            alerts.append(
                "Patient on anticoagulants — exercise caution with surgical procedures. "
                "Consult physician before extractions."
            )
        if "penicillin" in medical_history and "allergy" in medical_history:
            alerts.append(
                "Penicillin allergy noted — avoid amoxicillin. Use alternative antibiotics (e.g., clindamycin)."
            )
        if "swelling" in chief_complaint:
            alerts.append(
                "Swelling noted. Consider urgent clinical evaluation and rule out cellulitis."
            )
        if "hypertension" in medical_history or "blood pressure" in medical_history:
            alerts.append(
                "Hypertension noted — use local anaesthetic without epinephrine if BP is uncontrolled."
            )

        tooth_records = cls._get_tooth_records(consultation)
        conditions = [r.condition for r in tooth_records]

        if conditions.count("CARIES") >= 3:
            alerts.append(
                "Multiple caries detected. High caries-risk patient — fluoride therapy and dietary counselling recommended."
            )
        if "ROOT_STUMP" in conditions:
            alerts.append(
                "Root stump(s) present. Evaluate for extraction or root canal therapy."
            )
        if "MOBILE" in conditions:
            alerts.append(
                "Mobile tooth/teeth detected. Immediate periodontal evaluation required."
            )
        if "IMPACTED" in conditions:
            alerts.append(
                "Impacted tooth detected. Radiographic evaluation and surgical consultation recommended."
            )
        if "FRACTURED" in conditions:
            alerts.append(
                "Tooth fracture noted. Assess fracture line depth and restorability."
            )

        return alerts

    # ────────────────────────────────────────────────────────────────────────
    # Recommendation generation
    # ────────────────────────────────────────────────────────────────────────

    @classmethod
    def generate_recommendations(cls, consultation):
        department = cls.determine_department(consultation)
        recommendations = list(cls.DEPT_RECOMMENDATIONS.get(department, []))

        chief_complaint = cls._safe_lower(consultation.chief_complaint)

        # Cross-department supplemental recommendations
        if "swelling" in chief_complaint and department != CdssEngine.DEPT_ORAL_SURGERY:
            recommendations.append(
                "Consider antibiotics: Amoxicillin 500 mg TID for 5 days if infection is suspected."
            )
        if "bleeding" in chief_complaint and department != CdssEngine.DEPT_PERIODONTICS:
            recommendations.append(
                "Evaluate bleeding source. Rule out systemic cause (coagulopathy, medication)."
            )

        return recommendations

    # ────────────────────────────────────────────────────────────────────────
    # Diagnosis assistance text
    # ────────────────────────────────────────────────────────────────────────

    @classmethod
    def generate_diagnosis_assistance(cls, consultation, department):
        tooth_records = cls._get_tooth_records(consultation)

        condition_summary = ""
        if tooth_records:
            condition_counts: dict[str, int] = {}
            for record in tooth_records:
                condition_counts[record.condition] = (
                    condition_counts.get(record.condition, 0) + 1
                )
            parts = [
                f"{count} {cond.lower().replace('_', ' ')}"
                for cond, count in condition_counts.items()
            ]
            condition_summary = f" Dental chart findings: {', '.join(parts)}."

        dept_label = dict(CdssEngine.DEPT_CHOICES).get(department, "General Dentistry")
        chief_complaint = (consultation.chief_complaint or "Not specified").strip()

        return (
            f"Patient presents with: {chief_complaint}."
            f"{condition_summary}"
            f" Recommended department: {dept_label}."
            f" Further clinical evaluation is advised to confirm diagnosis and finalise the treatment plan."
        )

    # ────────────────────────────────────────────────────────────────────────
    # Recommendation row sync
    # ────────────────────────────────────────────────────────────────────────

    @staticmethod
    def sync_recommendation_rows(cdss_engine, recommendations):
        cdss_engine.cdss_recommendations.all().delete()
        for recommendation in recommendations:
            CdssRecommendation.objects.create(
                cdss_engine=cdss_engine,
                recommendation=recommendation,
                is_active=True,
            )

    # ────────────────────────────────────────────────────────────────────────
    # Build universal brain payload from structured wizard data
    # ────────────────────────────────────────────────────────────────────────

    @classmethod
    def _build_brain_payload(cls, consultation):
        """
        Constructs the payload dict for run_universal_brain() from
        the consultation's structured tooth_complaints and tooth tooth records.
        """
        # Patient info
        patient = consultation.patient
        age = 0
        if patient.date_of_birth:
            today = date.today()
            age = today.year - patient.date_of_birth.year - (
                (today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day)
            )

        # Allergies from structured consultation field
        allergies = [str(a).lower() for a in (consultation.allergies or [])]

        patient_payload = {"age": age, "allergy": allergies}

        history_payload = {
            "medical": list(consultation.systemic_conditions or []),
            "habits": list(consultation.habits or []),
            "pastDental": list(consultation.past_dental_history or []),
        }

        teeth_payload = {}

        # Load structured tooth complaints
        tooth_complaints = list(
            consultation.tooth_complaints.all()
        )

        for tc in tooth_complaints:
            tooth_no = str(tc.tooth_number)
            complaints = list(tc.complaint_codes or [])

            # Fetch exam_data from matching tooth record
            exam = {}
            try:
                dental_chart = consultation.dental_chart
                tooth_record = dental_chart.tooth_records.filter(
                    tooth_number=tooth_no, is_active=True
                ).first()
                if tooth_record:
                    exam = dict(tooth_record.exam_data or {})
            except Exception:
                pass

            teeth_payload[tooth_no] = {
                "complaints": complaints,
                "exam": exam,
            }

        return {
            "teeth": teeth_payload,
            "history": history_payload,
            "patient": patient_payload,
        }

    # ────────────────────────────────────────────────────────────────────────
    # Determine overall department from per-tooth results
    # ────────────────────────────────────────────────────────────────────────

    @classmethod
    def _department_from_brain_results(cls, per_tooth_results: dict):
        """
        Pick the primary department for the CdssEngine.department field.
        Strategy: use the department of the tooth with highest-confidence result.
        """
        from apps.cdss.engines.master_complaint_registry import MASTER_COMPLAINT_REGISTRY
        from apps.cdss.engines.universal_brain import ENGINE_MAP

        confidence_order = {"HIGH": 4, "MODERATE": 3, "LOW": 2, "VERY LOW": 1}

        best_dept = CdssEngine.DEPT_GENERAL
        best_score = 0

        dept_to_cdss_map = {
            "ENDO": CdssEngine.DEPT_ENDODONTICS,
            "PERIO": CdssEngine.DEPT_PERIODONTICS,
            "ORAL_MED": CdssEngine.DEPT_ORAL_SURGERY,
            "ORAL_SURGERY": CdssEngine.DEPT_ORAL_SURGERY,
            "CONSERVATIVE": CdssEngine.DEPT_GENERAL,
            "PROSTHODONTICS": CdssEngine.DEPT_PROSTHODONTICS,
            "ORTHODONTICS": CdssEngine.DEPT_ORTHODONTICS,
            "PEDODONTICS": CdssEngine.DEPT_PEDIATRIC,
            "IMPLANTOLOGY": CdssEngine.DEPT_PROSTHODONTICS,
        }

        for tooth_no, data in per_tooth_results.items():
            conf = confidence_order.get(data.get("confidence", "VERY LOW"), 1)
            if conf > best_score:
                best_score = conf
                # Try to determine department from ICD or diagnosis name
                icd = data.get("icd", "")
                diag = data.get("diagnosis", "") or ""
                if icd and icd.startswith("K04"):
                    best_dept = CdssEngine.DEPT_ENDODONTICS
                elif icd and icd.startswith("K05"):
                    best_dept = CdssEngine.DEPT_PERIODONTICS
                elif icd and icd.startswith("K07"):
                    best_dept = CdssEngine.DEPT_ORTHODONTICS
                elif icd and icd.startswith("Z46"):
                    best_dept = CdssEngine.DEPT_PROSTHODONTICS
                elif icd and icd.startswith("Z96"):
                    best_dept = CdssEngine.DEPT_PROSTHODONTICS
                elif icd and icd.startswith("K10"):
                    best_dept = CdssEngine.DEPT_ORAL_SURGERY
                elif icd and icd.startswith("K02"):
                    best_dept = CdssEngine.DEPT_GENERAL

        return best_dept

    # ────────────────────────────────────────────────────────────────────────
    # Analyse & update
    # ────────────────────────────────────────────────────────────────────────

    @classmethod
    @transaction.atomic
    def analyze_consultation(cls, consultation):
        """
        Runs the CDSS analysis. Uses the structured universal brain engine
        if tooth_complaints exist (wizard data), otherwise falls back to the
        legacy keyword-based analysis for backward compatibility.
        """
        has_structured_data = consultation.tooth_complaints.exists()

        if has_structured_data:
            # ── Structured path (wizard flow) ─────────────────────────────
            payload = cls._build_brain_payload(consultation)
            brain_output = run_universal_brain(payload)
            per_tooth_results = brain_output.get("teeth", {})

            department = cls._department_from_brain_results(per_tooth_results)
            risk_score = cls.calculate_risk_score(consultation)
            alerts = cls.generate_alerts(consultation)

            # Aggregate recommendations from all tooth results
            seen = set()
            recommendations = []
            for tooth_data in per_tooth_results.values():
                for step in (tooth_data.get("treatment") or []):
                    if step not in seen:
                        seen.add(step)
                        recommendations.append(step)
            if not recommendations:
                recommendations = cls.generate_recommendations(consultation)

            # Aggregate diagnosis text
            diag_parts = []
            icd_primary = None
            confidence_primary = None
            for tooth_no, tooth_data in per_tooth_results.items():
                diag = tooth_data.get("diagnosis")
                conf = tooth_data.get("confidence", "VERY LOW")
                icd = tooth_data.get("icd")
                if diag:
                    diag_parts.append(f"Tooth {tooth_no}: {diag} (ICD: {icd}, Confidence: {conf})")
                    if icd_primary is None:
                        icd_primary = icd
                        confidence_primary = conf

            diagnosis_assistance = "; ".join(diag_parts) if diag_parts else (
                cls.generate_diagnosis_assistance(consultation, department)
            )

        else:
            # ── Legacy path (free-text consultation) ─────────────────────
            department = cls.determine_department(consultation)
            risk_score = cls.calculate_risk_score(consultation)
            alerts = cls.generate_alerts(consultation)
            recommendations = cls.generate_recommendations(consultation)
            diagnosis_assistance = cls.generate_diagnosis_assistance(consultation, department)
            per_tooth_results = {}
            icd_primary = None
            confidence_primary = None

        cdss_engine, _created = CdssEngine.objects.update_or_create(
            consultation=consultation,
            defaults={
                "department": department,
                "risk_score": risk_score,
                "alerts": alerts,
                "recommendations": recommendations,
                "diagnosis_assistance": diagnosis_assistance,
                "icd_code": icd_primary,
                "confidence": confidence_primary,
                "per_tooth_results": per_tooth_results,
                "is_active": True,
            },
        )

        cls.sync_recommendation_rows(cdss_engine, recommendations)

        return cdss_engine

    @classmethod
    @transaction.atomic
    def update_cdss_engine(cls, cdss_engine_uuid, validated_data):
        cdss_engine = cls.get_cdss_engine_by_uuid(cdss_engine_uuid)

        if "department" in validated_data:
            cdss_engine.department = validated_data["department"]
        if "risk_score" in validated_data:
            cdss_engine.risk_score = validated_data["risk_score"]
        if "alerts" in validated_data:
            cdss_engine.alerts = validated_data["alerts"]
        if "recommendations" in validated_data:
            cdss_engine.recommendations = validated_data["recommendations"]
            cls.sync_recommendation_rows(cdss_engine, validated_data["recommendations"])
        if "diagnosis_assistance" in validated_data:
            cdss_engine.diagnosis_assistance = (
                validated_data.get("diagnosis_assistance", "").strip() or None
            )
        if "icd_code" in validated_data:
            cdss_engine.icd_code = validated_data["icd_code"]
        if "confidence" in validated_data:
            cdss_engine.confidence = validated_data["confidence"]
        if "is_active" in validated_data:
            cdss_engine.is_active = validated_data["is_active"]

        cdss_engine.save()
        return cdss_engine

    # ────────────────────────────────────────────────────────────────────────
    # Print report data
    # ────────────────────────────────────────────────────────────────────────

    @classmethod
    def get_cdss_print_data(cls, cdss_engine_uuid):
        cdss_engine = cls.get_cdss_engine_by_uuid(cdss_engine_uuid)
        return cdss_engine
