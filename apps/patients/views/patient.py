from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patients.serializers import PatientSerializer, PatientCreateSerializer
from apps.patients.services import PatientService


class PatientListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        patients = PatientService.list_patients()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PatientCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = PatientService.create_patient(serializer.validated_data)
        response_serializer = PatientSerializer(patient)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class PatientDetailAPIView(APIView):
    def get(self, request, patient_id, *args, **kwargs):
        patient = PatientService.get_patient_by_id(patient_id)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
