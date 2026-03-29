from rest_framework.exceptions import ValidationError

from apps.consultations.models import Consultation
from apps.odontology.models import DentalChart, ToothRecord


class OdontologyService:
    VALID_SURFACES = {
        "MESIAL",
        "DISTAL",
        "OCCLUSAL",
        "BUCCAL",
        "LINGUAL",
        "LABIAL",
        "INCISAL",
        "CERVICAL",
    }

    @staticmethod
    def get_consultation(consultation_id):
        try:
            return Consultation.objects.get(id=consultation_id, is_active=True)
        except Consultation.DoesNotExist:
            raise ValidationError(
                {"consultation_id": ["Valid active consultation not found."]}
            )

    @staticmethod
    def validate_chart_not_already_exists(consultation):
        if DentalChart.objects.filter(consultation=consultation).exists():
            raise ValidationError(
                {
                    "consultation_id": [
                        "A dental chart already exists for this consultation."
                    ]
                }
            )

    @staticmethod
    def get_chart(chart_id):
        try:
            return DentalChart.objects.select_related("consultation").get(
                id=chart_id, is_active=True
            )
        except DentalChart.DoesNotExist:
            raise ValidationError(
                {"chart_id": ["Valid active dental chart not found."]}
            )

    @staticmethod
    def validate_tooth_number(tooth_number: str):
        tooth_number = tooth_number.strip()
        if not tooth_number:
            raise ValidationError({"tooth_number": ["Tooth number is required."]})

        if len(tooth_number) > 10:
            raise ValidationError({"tooth_number": ["Tooth number is invalid."]})

    @classmethod
    def validate_surfaces(cls, surfaces):
        invalid_surfaces = [
            surface for surface in surfaces if surface.upper() not in cls.VALID_SURFACES
        ]
        if invalid_surfaces:
            raise ValidationError(
                {"surfaces": [f"Invalid surfaces: {', '.join(invalid_surfaces)}."]}
            )

    @staticmethod
    def validate_tooth_record_uniqueness(chart, tooth_number: str):
        if ToothRecord.objects.filter(
            chart=chart, tooth_number__iexact=tooth_number
        ).exists():
            raise ValidationError(
                {
                    "tooth_number": [
                        "A tooth record already exists for this tooth in the chart."
                    ]
                }
            )

    @classmethod
    def create_chart(cls, validated_data):
        consultation = cls.get_consultation(validated_data["consultation_id"])
        cls.validate_chart_not_already_exists(consultation)

        chart = DentalChart.objects.create(
            consultation=consultation,
            notes=validated_data.get("notes", "").strip() or None,
            is_active=validated_data.get("is_active", True),
        )
        return chart

    @staticmethod
    def list_charts():
        return (
            DentalChart.objects.select_related("consultation")
            .all()
            .order_by("-created_at")
        )

    @staticmethod
    def get_chart_by_id(chart_id):
        try:
            return (
                DentalChart.objects.select_related("consultation")
                .prefetch_related("tooth_records")
                .get(id=chart_id)
            )
        except DentalChart.DoesNotExist:
            raise ValidationError({"chart_id": ["Dental chart not found."]})

    @classmethod
    def create_tooth_record(cls, chart_id, validated_data):
        chart = cls.get_chart(chart_id)

        tooth_number = validated_data["tooth_number"].strip().upper()
        surfaces = [
            surface.strip().upper() for surface in validated_data.get("surfaces", [])
        ]

        cls.validate_tooth_number(tooth_number)
        cls.validate_surfaces(surfaces)
        cls.validate_tooth_record_uniqueness(chart, tooth_number)

        tooth_record = ToothRecord.objects.create(
            chart=chart,
            tooth_number=tooth_number,
            condition=validated_data["condition"],
            surfaces=surfaces,
            mobility_grade=validated_data.get("mobility_grade", "").strip() or None,
            percussion_tenderness=validated_data.get("percussion_tenderness", False),
            palpation_tenderness=validated_data.get("palpation_tenderness", False),
            probing_depth_summary=validated_data.get(
                "probing_depth_summary", ""
            ).strip()
            or None,
            notes=validated_data.get("notes", "").strip() or None,
            is_active=validated_data.get("is_active", True),
        )
        return tooth_record

    @staticmethod
    def list_tooth_records(chart_id):
        chart = OdontologyService.get_chart(chart_id)
        return chart.tooth_records.filter(is_active=True).order_by("tooth_number")
