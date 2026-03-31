from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "patient_code",
        "full_name",
        "gender",
        "phone_number",
        "email",
        "city",
        "is_active",
        "created_at",
    )

    list_filter = (
        "gender",
        "is_active",
        "city",
        "state",
        "country",
        "created_at",
    )

    search_fields = (
        "patient_code",
        "first_name",
        "last_name",
        "phone_number",
        "email",
    )

    ordering = ("-created_at",)

    readonly_fields = ("uuid", "created_at", "updated_at")

    list_editable = ("is_active",)

    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "uuid",
                    "patient_code",
                    "first_name",
                    "last_name",
                    "gender",
                    "date_of_birth",
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
            "Medical & Personal Info",
            {
                "fields": (
                    "blood_group",
                    "marital_status",
                    "occupation",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Emergency Contact",
            {
                "fields": (
                    "emergency_contact_name",
                    "emergency_contact_phone",
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

    def full_name(self, obj):
        return obj.full_name

    full_name.short_description = "Full Name"
