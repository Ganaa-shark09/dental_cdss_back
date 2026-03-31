from django.contrib import admin
from .models import Clinic


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "phone_number",
        "email",
        "city",
        "state",
        "country",
        "is_active",
    )

    list_filter = (
        "is_active",
        "city",
        "state",
        "country",
    )

    search_fields = (
        "name",
        "code",
        "phone_number",
        "email",
        "city",
    )

    ordering = ("name",)

    readonly_fields = ("uuid", "created_at", "updated_at")

    list_editable = ("is_active",)

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "uuid",
                    "name",
                    "code",
                    "is_active",
                )
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "phone_number",
                    "email",
                )
            },
        ),
        (
            "Address",
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "country",
                    "postal_code",
                ),
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
