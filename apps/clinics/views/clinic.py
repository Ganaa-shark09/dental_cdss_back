from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.audit_logs.services import AuditLogService
from apps.clinics.models import Clinic
from apps.clinics.serializers import ClinicSerializer, ClinicCreateSerializer
from apps.clinics.services import ClinicService


class ClinicListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        clinics = ClinicService.list_clinics()
        serializer = ClinicSerializer(clinics, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ClinicCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        clinic = ClinicService.create_clinic(serializer.validated_data, request.user)
        response_serializer = ClinicSerializer(clinic)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ClinicDetailAPIView(APIView):
    def get_object(self, uuid):
        return get_object_or_404(Clinic, uuid=uuid)

    def get(self, request, uuid, *args, **kwargs):
        clinic = self.get_object(uuid)
        serializer = ClinicSerializer(clinic)
        return Response(serializer.data)

    def put(self, request, uuid, *args, **kwargs):
        clinic = self.get_object(uuid)
        serializer = ClinicCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        code = validated_data["code"].strip().upper()

        if Clinic.objects.filter(code__iexact=code).exclude(uuid=clinic.uuid).exists():
            return Response(
                {"code": ["A clinic with this code already exists."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        clinic.name = validated_data["name"].strip()
        clinic.code = code
        clinic.email = validated_data.get("email") or None
        clinic.phone_number = validated_data.get("phone_number", "")
        clinic.address = validated_data.get("address", "")
        clinic.city = validated_data.get("city", "")
        clinic.state = validated_data.get("state", "")
        clinic.country = validated_data.get("country", "")
        clinic.postal_code = validated_data.get("postal_code", "")
        clinic.is_active = validated_data.get("is_active", True)
        clinic.save()

        AuditLogService.create_log(
            model_name="Clinic",
            record_id=clinic.uuid,
            field_name="updated",
            old_value=None,
            new_value=clinic.code,
            user=request.user,
        )

        response_serializer = ClinicSerializer(clinic)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, uuid, *args, **kwargs):
        clinic = self.get_object(uuid)
        serializer = ClinicCreateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        if "name" in validated_data:
            clinic.name = validated_data["name"].strip()

        if "code" in validated_data:
            code = validated_data["code"].strip().upper()
            if (
                Clinic.objects.filter(code__iexact=code)
                .exclude(uuid=clinic.uuid)
                .exists()
            ):
                return Response(
                    {"code": ["A clinic with this code already exists."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            clinic.code = code

        if "email" in validated_data:
            clinic.email = validated_data.get("email") or None
        if "phone_number" in validated_data:
            clinic.phone_number = validated_data.get("phone_number", "")
        if "address" in validated_data:
            clinic.address = validated_data.get("address", "")
        if "city" in validated_data:
            clinic.city = validated_data.get("city", "")
        if "state" in validated_data:
            clinic.state = validated_data.get("state", "")
        if "country" in validated_data:
            clinic.country = validated_data.get("country", "")
        if "postal_code" in validated_data:
            clinic.postal_code = validated_data.get("postal_code", "")
        if "is_active" in validated_data:
            clinic.is_active = validated_data["is_active"]

        clinic.save()

        AuditLogService.create_log(
            model_name="Clinic",
            record_id=clinic.uuid,
            field_name="updated",
            old_value=None,
            new_value=clinic.code,
            user=request.user,
        )

        response_serializer = ClinicSerializer(clinic)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, uuid, *args, **kwargs):
        clinic = self.get_object(uuid)
        clinic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
