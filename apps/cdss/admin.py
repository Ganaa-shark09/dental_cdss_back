from django.contrib import admin
from .models import CdssEngine, CdssRecommendation


class CdssRecommendationInline(admin.TabularInline):
    model = CdssRecommendation
    extra = 1
    fields = ("recommendation", "is_active", "created_at")
    readonly_fields = ("created_at",)


@admin.register(CdssEngine)
class CdssEngineAdmin(admin.ModelAdmin):
    list_display = (
        "consultation",
        "risk_score",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "consultation__consultation_number",
        "diagnosis_assistance",
    )

    ordering = ("-created_at",)

    readonly_fields = ("uuid", "created_at", "updated_at")

    autocomplete_fields = ("consultation",)

    inlines = [CdssRecommendationInline]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "uuid",
                    "consultation",
                    "risk_score",
                    "is_active",
                )
            },
        ),
        (
            "Clinical Decision Support",
            {
                "fields": (
                    "alerts",
                    "recommendations",
                    "diagnosis_assistance",
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


@admin.register(CdssRecommendation)
class CdssRecommendationAdmin(admin.ModelAdmin):
    list_display = (
        "cdss_engine",
        "short_recommendation",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "recommendation",
        "cdss_engine__consultation__consultation_number",
    )

    ordering = ("-created_at",)

    readonly_fields = ("uuid", "created_at", "updated_at")

    autocomplete_fields = ("cdss_engine",)

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "uuid",
                    "cdss_engine",
                    "recommendation",
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
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def short_recommendation(self, obj):
        return (
            (obj.recommendation[:50] + "...")
            if len(obj.recommendation) > 50
            else obj.recommendation
        )

    short_recommendation.short_description = "Recommendation"
