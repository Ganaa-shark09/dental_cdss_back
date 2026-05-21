from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models.fields import DateField, DateTimeField
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.patients.models.patient import Patient
from apps.appointments.models.appointment import Appointment
from apps.consultations.models.consultation import Consultation
from apps.audit_logs.models.audit_log import AuditLog
from apps.common.serializers import DashboardSummarySerializer

User = get_user_model()


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    APPOINTMENT_DATE_FIELDS = [
        "appointment_date",
        "scheduled_at",
        "scheduled_for",
        "start_time",
        "date",
        "created_at",
    ]

    COMPLETED_STATUSES = {
        "completed",
        "complete",
        "done",
        "closed",
        "finished",
    }

    def get(self, request):
        totals = self.get_totals()
        appointment_status_breakdown = self.get_appointment_status_breakdown(
            totals["appointments"]
        )

        data = {
            "totals": totals,
            "metrics": self.get_metrics(totals),
            "appointments_this_week": self.get_appointments_this_week(),
            "appointment_status_breakdown": appointment_status_breakdown,
            "clinical_snapshot": self.get_clinical_snapshot(
                totals=totals,
                appointment_status_breakdown=appointment_status_breakdown,
            ),
            "quick_links": self.get_quick_links(),
            "recent_activities": self.get_recent_activities(),
        }

        serializer = DashboardSummarySerializer(instance=data)
        return Response(serializer.data)

    def get_totals(self):
        return {
            "patients": Patient.objects.count(),
            "appointments": Appointment.objects.count(),
            "consultations": Consultation.objects.count(),
            "users": User.objects.count(),
        }

    def get_metrics(self, totals):
        return [
            {
                "key": "patients",
                "label": "Total Patients",
                "value": totals["patients"],
                "caption": "Registered patient records",
                "icon": "pi pi-users",
                "route": "/patients",
            },
            {
                "key": "appointments",
                "label": "Appointments",
                "value": totals["appointments"],
                "caption": "Scheduled appointment records",
                "icon": "pi pi-calendar",
                "route": "/appointments",
            },
            {
                "key": "consultations",
                "label": "Consultations",
                "value": totals["consultations"],
                "caption": "Clinical consultation entries",
                "icon": "pi pi-comments",
                "route": "/consultations",
            },
            {
                "key": "users",
                "label": "Users",
                "value": totals["users"],
                "caption": "System users",
                "icon": "pi pi-user",
                "route": "/users",
            },
        ]

    def get_quick_links(self):
        return [
            {
                "label": "Patients",
                "caption": "Manage patient records",
                "icon": "pi pi-users",
                "route": "/patients",
            },
            {
                "label": "Appointments",
                "caption": "Schedule and track visits",
                "icon": "pi pi-calendar",
                "route": "/appointments",
            },
            {
                "label": "Consultations",
                "caption": "Clinical consultation flow",
                "icon": "pi pi-comments",
                "route": "/consultations",
            },
            {
                "label": "CDSS",
                "caption": "Decision support system",
                "icon": "pi pi-bolt",
                "route": "/cdss",
            },
        ]

    def get_appointments_this_week(self):
        field_name, field = self.get_appointment_date_field()

        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())
        week_days = [week_start + timedelta(days=index) for index in range(7)]

        empty_week = [
            {
                "day": day.strftime("%a"),
                "date": day,
                "count": 0,
            }
            for day in week_days
        ]

        if not field_name:
            return empty_week

        if isinstance(field, DateTimeField):
            date_filter = {f"{field_name}__date__range": [week_days[0], week_days[-1]]}
        else:
            date_filter = {f"{field_name}__range": [week_days[0], week_days[-1]]}

        weekly_rows = (
            Appointment.objects.filter(**date_filter)
            .annotate(day_date=TruncDate(field_name))
            .values("day_date")
            .annotate(count=Count("id"))
            .order_by("day_date")
        )

        count_by_day = {
            row["day_date"]: row["count"] for row in weekly_rows if row["day_date"]
        }

        return [
            {
                "day": day.strftime("%a"),
                "date": day,
                "count": count_by_day.get(day, 0),
            }
            for day in week_days
        ]

    def get_appointment_status_breakdown(self, total_appointments):
        if not self.model_has_field(Appointment, "status"):
            return []

        rows = (
            Appointment.objects.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )

        result = []

        for row in rows:
            count = row["count"]
            status = row["status"] or "Unknown"

            percentage = (
                round((count / total_appointments) * 100, 2)
                if total_appointments
                else 0
            )

            result.append(
                {
                    "status": str(status),
                    "count": count,
                    "percentage": percentage,
                }
            )

        return result

    def get_clinical_snapshot(self, totals, appointment_status_breakdown):
        total_records = (
            totals["patients"]
            + totals["appointments"]
            + totals["consultations"]
            + totals["users"]
        )

        completion_rate = self.get_completion_rate(
            total_appointments=totals["appointments"],
            total_consultations=totals["consultations"],
            appointment_status_breakdown=appointment_status_breakdown,
        )

        return {
            "total_records": total_records,
            "completion_rate": completion_rate,
            "last_updated": timezone.now(),
        }

    def get_completion_rate(
        self,
        total_appointments,
        total_consultations,
        appointment_status_breakdown,
    ):
        if not total_appointments:
            return 0

        completed_count = 0

        for item in appointment_status_breakdown:
            status = item["status"].lower()

            if status in self.COMPLETED_STATUSES:
                completed_count += item["count"]

        if completed_count:
            return round((completed_count / total_appointments) * 100, 2)

        return round(
            (min(total_consultations, total_appointments) / total_appointments) * 100,
            2,
        )

    def get_recent_activities(self):
        logs = AuditLog.objects.select_related("user").order_by("-timestamp")[:5]

        return [
            {
                "model": log.model_name,
                "field": log.field_name,
                "old": self.clean_value(log.old_value),
                "new": self.clean_value(log.new_value),
                "user": str(log.user) if log.user_id else "System",
                "timestamp": log.timestamp,
            }
            for log in logs
        ]

    def get_appointment_date_field(self):
        for field_name in self.APPOINTMENT_DATE_FIELDS:
            try:
                field = Appointment._meta.get_field(field_name)

                if isinstance(field, (DateTimeField, DateField)):
                    return field_name, field

            except Exception:
                continue

        return None, None

    def model_has_field(self, model, field_name):
        try:
            model._meta.get_field(field_name)
            return True
        except Exception:
            return False

    def clean_value(self, value):
        if value is None:
            return None

        return str(value)
