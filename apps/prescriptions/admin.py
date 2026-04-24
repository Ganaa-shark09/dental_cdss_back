from django.contrib import admin
from .models import Prescription


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "patient",
        "consultation",
        "medication",
        "dosage",
        "date_issued",
        "expiry_date",
        "is_active",
    )
    list_filter = (
        "is_active",
        "date_issued",
        "expiry_date",
    )
    search_fields = (
        "uuid",
        "patient__full_name",
        "consultation__consultation_number",
        "medication",
    )
    readonly_fields = ("uuid", "created_at", "updated_at")
    date_hierarchy = "date_issued"

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "uuid",
                    "patient",
                    "consultation",
                    "medication",
                    "dosage",
                )
            },
        ),
        (
            "Treatment Details",
            {
                "fields": (
                    "treatment_instructions",
                    "notes",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "date_issued",
                    "expiry_date",
                )
            },
        ),
        ("Status", {"fields": ("is_active",)}),
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
