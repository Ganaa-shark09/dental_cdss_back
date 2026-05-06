from rest_framework.exceptions import ValidationError

from apps.audit_logs.services import AuditLogService
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
    def get_consultation(consultation_uuid):
        try:
            return Consultation.objects.get(uuid=consultation_uuid, is_active=True)
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
    def get_chart(chart_uuid):
        try:
            return DentalChart.objects.select_related("consultation").get(
                uuid=chart_uuid,
                is_active=True,
            )
        except DentalChart.DoesNotExist:
            raise ValidationError(
                {"chart_uuid": ["Valid active dental chart not found."]}
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
    def validate_tooth_record_uniqueness(chart, tooth_number: str, exclude_uuid=None):
        qs = ToothRecord.objects.filter(chart=chart, tooth_number__iexact=tooth_number)
        if exclude_uuid:
            qs = qs.exclude(uuid=exclude_uuid)

        if qs.exists():
            raise ValidationError(
                {
                    "tooth_number": [
                        "A tooth record already exists for this tooth in the chart."
                    ]
                }
            )

    @classmethod
    def create_chart(cls, validated_data, user):
        consultation = cls.get_consultation(validated_data["consultation_id"])
        cls.validate_chart_not_already_exists(consultation)

        chart = DentalChart.objects.create(
            consultation=consultation,
            notes=validated_data.get("notes", "").strip() or None,
            is_active=validated_data.get("is_active", True),
        )

        AuditLogService.create_log(
            model_name="DentalChart",
            record_id=chart.uuid,
            field_name="created",
            old_value=None,
            new_value=f"Consultation {consultation.uuid}",
            user=user,
        )

        return chart

    @staticmethod
    def list_charts():
        return (
            DentalChart.objects.select_related("consultation")
            .prefetch_related("tooth_records")
            .all()
            .order_by("-created_at")
        )

    @staticmethod
    def get_chart_by_uuid(chart_uuid):
        try:
            return (
                DentalChart.objects.select_related("consultation")
                .prefetch_related("tooth_records")
                .get(uuid=chart_uuid)
            )
        except DentalChart.DoesNotExist:
            raise ValidationError({"chart_uuid": ["Dental chart not found."]})

    @classmethod
    def update_chart(cls, chart_uuid, validated_data, user):
        chart = cls.get_chart_by_uuid(chart_uuid)

        old_values = {
            "notes": chart.notes,
            "is_active": chart.is_active,
        }

        if "notes" in validated_data:
            chart.notes = validated_data.get("notes", "").strip() or None

        if "is_active" in validated_data:
            chart.is_active = validated_data["is_active"]

        chart.save()

        new_values = {
            "notes": chart.notes,
            "is_active": chart.is_active,
        }

        for field_name, old_val in old_values.items():
            new_val = new_values[field_name]
            if str(old_val) != str(new_val):
                AuditLogService.create_log(
                    model_name="DentalChart",
                    record_id=chart.uuid,
                    field_name=field_name,
                    old_value=old_val,
                    new_value=new_val,
                    user=user,
                )

        return chart

    @staticmethod
    def get_tooth_record(chart_uuid, tooth_record_uuid):
        try:
            return ToothRecord.objects.select_related(
                "chart", "chart__consultation"
            ).get(
                uuid=tooth_record_uuid,
                chart__uuid=chart_uuid,
            )
        except ToothRecord.DoesNotExist:
            raise ValidationError({"tooth_record_uuid": ["Tooth record not found."]})

    @classmethod
    def create_tooth_record(cls, chart_uuid, validated_data, user):
        chart = cls.get_chart(chart_uuid)

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

        AuditLogService.create_log(
            model_name="ToothRecord",
            record_id=tooth_record.uuid,
            field_name="created",
            old_value=None,
            new_value=f"Tooth {tooth_number} - {tooth_record.condition}",
            user=user,
        )

        return tooth_record

    @staticmethod
    def list_tooth_records(chart_uuid):
        chart = OdontologyService.get_chart(chart_uuid)
        return chart.tooth_records.filter(is_active=True).order_by("tooth_number")

    @classmethod
    def update_tooth_record(cls, chart_uuid, tooth_record_uuid, validated_data, user):
        tooth_record = cls.get_tooth_record(chart_uuid, tooth_record_uuid)

        old_values = {
            "surfaces": str(tooth_record.surfaces),
            "condition": tooth_record.condition,
            "mobility_grade": tooth_record.mobility_grade,
            "percussion_tenderness": tooth_record.percussion_tenderness,
            "palpation_tenderness": tooth_record.palpation_tenderness,
            "probing_depth_summary": tooth_record.probing_depth_summary,
            "notes": tooth_record.notes,
            "is_active": tooth_record.is_active,
        }

        if "surfaces" in validated_data:
            surfaces = [
                surface.strip().upper()
                for surface in validated_data.get("surfaces", [])
            ]
            cls.validate_surfaces(surfaces)
            tooth_record.surfaces = surfaces

        if "condition" in validated_data:
            tooth_record.condition = validated_data["condition"]

        if "mobility_grade" in validated_data:
            tooth_record.mobility_grade = (
                validated_data.get("mobility_grade", "").strip() or None
            )

        if "percussion_tenderness" in validated_data:
            tooth_record.percussion_tenderness = validated_data["percussion_tenderness"]

        if "palpation_tenderness" in validated_data:
            tooth_record.palpation_tenderness = validated_data["palpation_tenderness"]

        if "probing_depth_summary" in validated_data:
            tooth_record.probing_depth_summary = (
                validated_data.get("probing_depth_summary", "").strip() or None
            )

        if "notes" in validated_data:
            tooth_record.notes = validated_data.get("notes", "").strip() or None

        if "is_active" in validated_data:
            tooth_record.is_active = validated_data["is_active"]

        tooth_record.save()

        new_values = {
            "surfaces": str(tooth_record.surfaces),
            "condition": tooth_record.condition,
            "mobility_grade": tooth_record.mobility_grade,
            "percussion_tenderness": tooth_record.percussion_tenderness,
            "palpation_tenderness": tooth_record.palpation_tenderness,
            "probing_depth_summary": tooth_record.probing_depth_summary,
            "notes": tooth_record.notes,
            "is_active": tooth_record.is_active,
        }

        for field_name, old_val in old_values.items():
            new_val = new_values[field_name]
            if str(old_val) != str(new_val):
                AuditLogService.create_log(
                    model_name="ToothRecord",
                    record_id=tooth_record.uuid,
                    field_name=field_name,
                    old_value=old_val,
                    new_value=new_val,
                    user=user,
                )

        return tooth_record
