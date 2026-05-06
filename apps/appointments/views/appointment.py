from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.appointments.serializers import (
    AppointmentSerializer,
    AppointmentCreateSerializer,
)
from apps.appointments.services import AppointmentService


class AppointmentListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        appointments = AppointmentService.list_appointments()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = AppointmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appointment = AppointmentService.create_appointment(serializer.validated_data, request.user)
        response_serializer = AppointmentSerializer(appointment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class AppointmentDetailAPIView(APIView):
    def get(self, request, appointment_id, *args, **kwargs):
        appointment = AppointmentService.get_appointment_by_id(appointment_id)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
