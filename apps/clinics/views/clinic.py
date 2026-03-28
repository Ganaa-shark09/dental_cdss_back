from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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

        clinic = ClinicService.create_clinic(serializer.validated_data)
        response_serializer = ClinicSerializer(clinic)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
