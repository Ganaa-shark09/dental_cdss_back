from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.prescriptions.serializers import (
    PrescriptionSerializer,
    PrescriptionCreateSerializer,
)
from apps.prescriptions.services import PrescriptionService
from apps.prescriptions.models import Prescription


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
    def get(self, request, prescription_id, *args, **kwargs):
        try:
            prescription = Prescription.objects.get(id=prescription_id)
            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data)
        except Prescription.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
