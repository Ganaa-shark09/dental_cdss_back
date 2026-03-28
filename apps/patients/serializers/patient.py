from rest_framework import serializers
from apps.patients.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        fields = (
            "uuid",
            "patient_code",
            "first_name",
            "last_name",
            "full_name",
            "gender",
            "date_of_birth",
            "phone_number",
            "email",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "blood_group",
            "marital_status",
            "occupation",
            "emergency_contact_name",
            "emergency_contact_phone",
            "is_active",
            "created_at",
            "updated_at",
        )


class PatientCreateSerializer(serializers.Serializer):
    patient_code = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=["MALE", "FEMALE", "OTHER"])
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    phone_number = serializers.CharField(
        max_length=20, required=False, allow_blank=True
    )
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)

    address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    postal_code = serializers.CharField(max_length=20, required=False, allow_blank=True)

    blood_group = serializers.CharField(max_length=10, required=False, allow_blank=True)
    marital_status = serializers.CharField(
        max_length=50, required=False, allow_blank=True
    )
    occupation = serializers.CharField(max_length=150, required=False, allow_blank=True)

    emergency_contact_name = serializers.CharField(
        max_length=150, required=False, allow_blank=True
    )
    emergency_contact_phone = serializers.CharField(
        max_length=20, required=False, allow_blank=True
    )

    is_active = serializers.BooleanField(required=False, default=True)
