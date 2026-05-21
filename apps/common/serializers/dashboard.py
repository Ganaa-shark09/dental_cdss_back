from rest_framework import serializers


class TotalsSerializer(serializers.Serializer):
    patients = serializers.IntegerField()
    appointments = serializers.IntegerField()
    consultations = serializers.IntegerField()
    users = serializers.IntegerField()


class MetricSerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()
    value = serializers.IntegerField()
    caption = serializers.CharField()
    icon = serializers.CharField()
    route = serializers.CharField()


class WeeklyAppointmentSerializer(serializers.Serializer):
    day = serializers.CharField()
    date = serializers.DateField()
    count = serializers.IntegerField()


class StatusBreakdownSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()


class ClinicalSnapshotSerializer(serializers.Serializer):
    total_records = serializers.IntegerField()
    completion_rate = serializers.FloatField()
    last_updated = serializers.DateTimeField()


class QuickLinkSerializer(serializers.Serializer):
    label = serializers.CharField()
    caption = serializers.CharField()
    icon = serializers.CharField()
    route = serializers.CharField()


class ActivitySerializer(serializers.Serializer):
    model = serializers.CharField()
    field = serializers.CharField()
    old = serializers.CharField(allow_null=True, allow_blank=True)
    new = serializers.CharField(allow_null=True, allow_blank=True)
    user = serializers.CharField()
    timestamp = serializers.DateTimeField()


class DashboardSummarySerializer(serializers.Serializer):
    totals = TotalsSerializer()
    metrics = MetricSerializer(many=True)
    appointments_this_week = WeeklyAppointmentSerializer(many=True)
    appointment_status_breakdown = StatusBreakdownSerializer(many=True)
    clinical_snapshot = ClinicalSnapshotSerializer()
    quick_links = QuickLinkSerializer(many=True)
    recent_activities = ActivitySerializer(many=True)
