from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "document_type",
        "consultation",
        "file_link",
        "is_active",
        "created_at",
    )

    list_filter = (
        "document_type",
        "is_active",
        "created_at",
    )

    search_fields = (
        "document_type",
        "consultation__consultation_number",
        "description",
    )

    ordering = ("-created_at",)

    readonly_fields = ("uuid", "created_at", "updated_at", "file_preview")

    autocomplete_fields = ("consultation",)

    list_editable = ("is_active",)

    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "uuid",
                    "document_type",
                    "consultation",
                    "is_active",
                )
            },
        ),
        (
            "File",
            {
                "fields": (
                    "document",
                    "file_preview",
                    "description",
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

    def file_link(self, obj):
        if obj.document:
            return f'<a href="{obj.document.url}" target="_blank">View</a>'
        return "-"

    file_link.allow_tags = True
    file_link.short_description = "File"

    def file_preview(self, obj):
        if obj.document:
            return f'<a href="{obj.document.url}" target="_blank">Open File</a>'
        return "No file uploaded"

    file_preview.allow_tags = True
    file_preview.short_description = "Preview"
