from django.contrib import admin
from .models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        "consultation_number",
        "patient",
        "clinic",
        "staff_profile",
        "consultation_date",
        "consultation_time",
        "status",
        "is_active",
    )

    list_filter = (
        "status",
        "is_active",
        "consultation_date",
        "clinic",
    )

    search_fields = (
        "consultation_number",
        "patient__first_name",
        "patient__last_name",
        "clinic__name",
        "staff_profile__user__first_name",
        "staff_profile__user__last_name",
    )

    ordering = ("-consultation_date", "-consultation_time")

    readonly_fields = ("uuid", "created_at", "updated_at")

    autocomplete_fields = ("appointment", "patient", "clinic", "staff_profile")

    date_hierarchy = "consultation_date"

    list_editable = ("status", "is_active")

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "uuid",
                    "consultation_number",
                    "status",
                    "is_active",
                )
            },
        ),
        (
            "Relationships",
            {
                "fields": (
                    "appointment",
                    "patient",
                    "clinic",
                    "staff_profile",
                )
            },
        ),
        (
            "Schedule",
            {
                "fields": (
                    "consultation_date",
                    "consultation_time",
                )
            },
        ),
        (
            "Clinical Notes",
            {
                "fields": (
                    "chief_complaint",
                    "history_of_present_illness",
                    "medical_history_summary",
                    "dental_history_summary",
                    "examination_summary",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Diagnosis",
            {
                "fields": (
                    "provisional_diagnosis",
                    "final_diagnosis",
                )
            },
        ),
        (
            "Additional Notes",
            {
                "fields": ("notes",),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
