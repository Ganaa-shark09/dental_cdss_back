from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "model_name",
        "record_id",
        "field_name",
        "user",
        "timestamp",
    )

    list_filter = (
        "model_name",
        "field_name",
        "user",
        "timestamp",
    )

    search_fields = (
        "model_name",
        "field_name",
        "old_value",
        "new_value",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    ordering = ("-timestamp",)

    readonly_fields = (
        "model_name",
        "record_id",
        "field_name",
        "old_value",
        "new_value",
        "user",
        "timestamp",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "timestamp"

    fieldsets = (
        (
            "Change Info",
            {
                "fields": (
                    "model_name",
                    "record_id",
                    "field_name",
                )
            },
        ),
        (
            "Values",
            {
                "fields": (
                    "old_value",
                    "new_value",
                )
            },
        ),
        (
            "User & Time",
            {
                "fields": (
                    "user",
                    "timestamp",
                )
            },
        ),
        (
            "System Fields",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def has_add_permission(self, request):
        return False  # Prevent manual creation

    def has_change_permission(self, request, obj=None):
        return False  # Prevent edits

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion (optional, remove if you want cleanup)
