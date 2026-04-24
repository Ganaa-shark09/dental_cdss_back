from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.consultations.models import Consultation
from apps.cdss.models import CdssEngine, CdssRecommendation


class CdssService:
    @staticmethod
    def get_consultation(consultation_uuid):
        try:
            return Consultation.objects.get(uuid=consultation_uuid, is_active=True)
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid consultation not found."]}
            )

    @staticmethod
    def get_cdss_engine_by_uuid(cdss_engine_uuid):
        try:
            return CdssEngine.objects.select_related("consultation").get(
                uuid=cdss_engine_uuid
            )
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
    def calculate_risk_score(cls, consultation):
        risk_score = Decimal("0.00")

        chief_complaint = cls._safe_lower(consultation.chief_complaint)
        medical_history = cls._safe_lower(consultation.medical_history_summary)

        if "pain" in chief_complaint:
            risk_score += Decimal("5.00")

        if "infection" in medical_history:
            risk_score += Decimal("3.00")

        return risk_score

    @classmethod
    def generate_alerts(cls, consultation):
        alerts = []

        medical_history = cls._safe_lower(consultation.medical_history_summary)
        chief_complaint = cls._safe_lower(consultation.chief_complaint)

        if "infection" in medical_history:
            alerts.append("Risk of infection due to existing conditions.")

        if "swelling" in chief_complaint:
            alerts.append("Swelling noted. Consider urgent clinical evaluation.")

        return alerts

    @classmethod
    def generate_recommendations(cls, consultation):
        recommendations = []

        chief_complaint = cls._safe_lower(consultation.chief_complaint)

        if "tooth pain" in chief_complaint:
            recommendations.append("Consider prescribing pain relievers.")

        if "bleeding" in chief_complaint:
            recommendations.append(
                "Evaluate periodontal condition and bleeding source."
            )

        if not recommendations:
            recommendations.append("Proceed with standard clinical evaluation.")

        return recommendations

    @staticmethod
    def sync_recommendation_rows(cdss_engine, recommendations):
        cdss_engine.cdss_recommendations.all().delete()

        for recommendation in recommendations:
            CdssRecommendation.objects.create(
                cdss_engine=cdss_engine,
                recommendation=recommendation,
                is_active=True,
            )

    @classmethod
    @transaction.atomic
    def analyze_consultation(cls, consultation):
        risk_score = cls.calculate_risk_score(consultation)
        alerts = cls.generate_alerts(consultation)
        recommendations = cls.generate_recommendations(consultation)

        cdss_engine, _created = CdssEngine.objects.update_or_create(
            consultation=consultation,
            defaults={
                "risk_score": risk_score,
                "alerts": alerts,
                "recommendations": recommendations,
                "diagnosis_assistance": "Suggest further evaluation of symptoms.",
                "is_active": True,
            },
        )

        cls.sync_recommendation_rows(cdss_engine, recommendations)

        return cdss_engine

    @classmethod
    @transaction.atomic
    def update_cdss_engine(cls, cdss_engine_uuid, validated_data):
        cdss_engine = cls.get_cdss_engine_by_uuid(cdss_engine_uuid)

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

        if "is_active" in validated_data:
            cdss_engine.is_active = validated_data["is_active"]

        cdss_engine.save()
        return cdss_engine
