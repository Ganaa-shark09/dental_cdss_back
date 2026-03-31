from django.contrib import admin
from .models import StaffProfile


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "user",
        "clinic",
        "designation",
        "specialization",
        "years_of_experience",
        "is_active",
    )

    list_filter = (
        "designation",
        "specialization",
        "clinic",
        "is_active",
    )

    search_fields = (
        "employee_id",
        "user__first_name",
        "user__last_name",
        "user__email",
        "clinic__name",
        "designation",
        "specialization",
    )

    ordering = ("designation", "employee_id")

    readonly_fields = ("uuid", "created_at", "updated_at")

    list_editable = ("is_active",)

    autocomplete_fields = ("user", "clinic")

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "uuid",
                    "user",
                    "clinic",
                    "employee_id",
                    "designation",
                    "is_active",
                )
            },
        ),
        (
            "Professional Details",
            {
                "fields": (
                    "specialization",
                    "license_number",
                    "years_of_experience",
                )
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
