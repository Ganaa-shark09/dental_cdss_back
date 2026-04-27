from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.prescriptions.serializers import (
    PrescriptionSerializer,
    PrescriptionCreateSerializer,
    PrescriptionUpdateSerializer,
    PrescriptionPrintSerializer,
)
from apps.prescriptions.services import PrescriptionService


class PrescriptionListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        prescriptions = PrescriptionService.list_prescriptions()
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PrescriptionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prescription = PrescriptionService.create_prescription(
            serializer.validated_data
        )
        response_serializer = PrescriptionSerializer(prescription)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class PrescriptionDetailAPIView(APIView):
    def get(self, request, prescription_uuid, *args, **kwargs):
        prescription = PrescriptionService.get_prescription_by_uuid(prescription_uuid)
        serializer = PrescriptionSerializer(prescription)
        return Response(serializer.data)

    def put(self, request, prescription_uuid, *args, **kwargs):
        serializer = PrescriptionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prescription = PrescriptionService.update_prescription(
            prescription_uuid, serializer.validated_data
        )
        response_serializer = PrescriptionSerializer(prescription)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, prescription_uuid, *args, **kwargs):
        serializer = PrescriptionUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        prescription = PrescriptionService.update_prescription(
            prescription_uuid, serializer.validated_data
        )
        response_serializer = PrescriptionSerializer(prescription)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class PrescriptionPrintAPIView(APIView):
    def get(self, request, prescription_uuid, *args, **kwargs):
        prescription = PrescriptionService.get_prescription_by_uuid(prescription_uuid)
        serializer = PrescriptionPrintSerializer(prescription)
        return Response(serializer.data)
