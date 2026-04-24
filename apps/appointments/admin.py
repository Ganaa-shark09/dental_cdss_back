from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "appointment_number",
        "patient",
        "clinic",
        "staff_profile",
        "appointment_date",
        "appointment_time",
        "status",
        "is_active",
    )

    list_filter = (
        "status",
        "is_active",
        "appointment_date",
        "clinic",
    )

    search_fields = (
        "appointment_number",
        "patient__full_name",
        "clinic__name",
        "staff_profile__user__first_name",
        "staff_profile__user__last_name",
    )

    ordering = ("-appointment_date", "-appointment_time")

    readonly_fields = ("uuid",)

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "uuid",
                    "appointment_number",
                    "status",
                    "is_active",
                )
            },
        ),
        (
            "Relationships",
            {
                "fields": (
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
                    "appointment_date",
                    "appointment_time",
                )
            },
        ),
        (
            "Additional Details",
            {
                "fields": (
                    "reason_for_visit",
                    "notes",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    autocomplete_fields = ("patient", "clinic", "staff_profile")
