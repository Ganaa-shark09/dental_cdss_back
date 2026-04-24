from django.contrib import admin
from .models import TreatmentPlan


@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "consultation",
        "treatment_type",
        "status",
        "start_date",
        "end_date",
        "is_active",
        "created_at",
    )
    list_filter = (
        "status",
        "is_active",
        "start_date",
        "end_date",
        "created_at",
    )
    search_fields = (
        "uuid",
        "consultation__consultation_number",
        "treatment_type",
        "treatment_description",
    )
    readonly_fields = ("uuid", "created_at", "updated_at")
    list_editable = ("status", "is_active")
    ordering = ("-created_at",)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "uuid",
                    "consultation",
                    "treatment_type",
                    "treatment_description",
                )
            },
        ),
        (
            "Schedule & Status",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "status",
                    "is_active",
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
