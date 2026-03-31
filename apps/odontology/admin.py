from django.contrib import admin
from .models import DentalChart, ToothRecord


class ToothRecordInline(admin.TabularInline):
    model = ToothRecord
    extra = 0
    fields = (
        "tooth_number",
        "condition",
        "surfaces",
        "mobility_grade",
        "percussion_tenderness",
        "palpation_tenderness",
        "probing_depth_summary",
        "notes",
        "is_active",
    )
    show_change_link = True


@admin.register(DentalChart)
class DentalChartAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "consultation",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("uuid", "consultation__consultation_number")
    readonly_fields = ("uuid", "created_at", "updated_at")
    inlines = [ToothRecordInline]


@admin.register(ToothRecord)
class ToothRecordAdmin(admin.ModelAdmin):
    list_display = (
        "tooth_number",
        "chart",
        "condition",
        "is_active",
        "created_at",
    )
    list_filter = (
        "condition",
        "is_active",
        "percussion_tenderness",
        "palpation_tenderness",
    )
    search_fields = (
        "tooth_number",
        "chart__consultation__consultation_number",
    )
    readonly_fields = ("uuid", "created_at", "updated_at")
