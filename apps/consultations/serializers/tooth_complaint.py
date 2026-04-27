from rest_framework import serializers

from apps.consultations.models import ToothComplaint


class ToothComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToothComplaint
        fields = (
            "uuid",
            "consultation",
            "tooth_number",
            "complaint_codes",
            "duration",
            "severity",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("uuid", "consultation", "created_at", "updated_at")


class ToothComplaintCreateSerializer(serializers.Serializer):
    tooth_number = serializers.CharField(max_length=10)
    complaint_codes = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    duration = serializers.CharField(max_length=50, required=False, allow_blank=True)
    severity = serializers.CharField(max_length=20, required=False, allow_blank=True)


class ToothComplaintBulkCreateSerializer(serializers.Serializer):
    """
    Accepts a list of per-tooth complaint objects in one request.
    Useful for the wizard step that saves all tooth complaints at once.
    """
    teeth = ToothComplaintCreateSerializer(many=True)


class ToothComplaintUpdateSerializer(serializers.Serializer):
    complaint_codes = serializers.ListField(child=serializers.DictField(), required=False)
    duration = serializers.CharField(max_length=50, required=False, allow_blank=True)
    severity = serializers.CharField(max_length=20, required=False, allow_blank=True)
