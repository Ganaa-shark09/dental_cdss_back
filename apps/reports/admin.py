from django.contrib import admin
from .models import Report
from apps.documents.models import Document


class DocumentInline(admin.TabularInline):
    model = Report.documents.through
    extra = 0
    verbose_name = "Document"
    verbose_name_plural = "Documents"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "consultation",
        "report_type",
        "prescription_summary",
        "treatment_plan_summary",
        "is_active",
        "created_at",
    )
    list_filter = (
        "is_active",
        "report_type",
        "created_at",
    )
    search_fields = (
        "uuid",
        "consultation__consultation_number",
        "report_type",
        "prescription_summary__medication",
        "treatment_plan_summary__title",
    )
    readonly_fields = ("uuid", "created_at", "updated_at")
    inlines = [DocumentInline]
    filter_horizontal = ("documents",)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "uuid",
                    "consultation",
                    "report_type",
                    "is_active",
                )
            },
        ),
        (
            "Summaries",
            {
                "fields": (
                    "prescription_summary",
                    "treatment_plan_summary",
                )
            },
        ),
        (
            "Documents & Notes",
            {
                "fields": (
                    "documents",
                    "notes",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
