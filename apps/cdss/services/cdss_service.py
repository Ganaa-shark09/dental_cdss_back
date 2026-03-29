from rest_framework.exceptions import ValidationError

from apps.consultations.models import Consultation
from apps.cdss.models import CdssEngine, CdssRecommendation


class CdssService:
    @staticmethod
    def get_consultation(consultation_id):
        try:
            return Consultation.objects.get(id=consultation_id, is_active=True)
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid consultation not found."]}
            )

    @classmethod
    def analyze_consultation(cls, consultation):
        # Step 1: Calculate risk score (example)
        risk_score = cls.calculate_risk_score(consultation)

        # Step 2: Generate alerts (example)
        alerts = cls.generate_alerts(consultation)

        # Step 3: Generate recommendations (example)
        recommendations = cls.generate_recommendations(consultation)

        # Step 4: Create a CDSS engine entry
        cdss_engine = CdssEngine.objects.create(
            consultation=consultation,
            risk_score=risk_score,
            alerts=alerts,
            recommendations=recommendations,
            diagnosis_assistance="Suggest further evaluation of symptoms.",
            is_active=True,
        )

        # Step 5: Create recommendations entries
        cls.create_recommendations(cdss_engine, recommendations)

        return cdss_engine

    @staticmethod
    def calculate_risk_score(consultation):
        # This is just a dummy example of risk calculation
        risk_score = 0
        if "pain" in consultation.chief_complaint.lower():
            risk_score += 5
        return risk_score

    @staticmethod
    def generate_alerts(consultation):
        alerts = []
        if "infection" in consultation.medical_history_summary.lower():
            alerts.append("Risk of infection due to existing conditions.")
        return alerts

    @staticmethod
    def generate_recommendations(consultation):
        recommendations = []
        if "tooth pain" in consultation.chief_complaint.lower():
            recommendations.append("Consider prescribing pain relievers.")
        return recommendations

    @staticmethod
    def create_recommendations(cdss_engine, recommendations):
        for recommendation in recommendations:
            CdssRecommendation.objects.create(
                cdss_engine=cdss_engine,
                recommendation=recommendation,
                is_active=True,
            )

    @staticmethod
    def list_cdss_engines():
        return CdssEngine.objects.all().order_by("-created_at")

    @staticmethod
    def get_cdss_engine_by_id(cdss_engine_id):
        try:
            return CdssEngine.objects.get(id=cdss_engine_id)
        except CdssEngine.DoesNotExist:
            raise ValidationError({"cdss_engine_id": ["CDSS engine not found."]})
