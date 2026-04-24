from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.consultations.serializers import (
    ConsultationSerializer,
    ConsultationCreateSerializer,
    ConsultationUpdateSerializer,
)
from apps.consultations.services import ConsultationService


class ConsultationListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        consultations = ConsultationService.list_consultations()
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ConsultationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        consultation = ConsultationService.create_consultation(
            serializer.validated_data
        )
        response_serializer = ConsultationSerializer(consultation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ConsultationDetailAPIView(APIView):
    def get(self, request, consultation_id, *args, **kwargs):
        consultation = ConsultationService.get_consultation_by_id(consultation_id)
        serializer = ConsultationSerializer(consultation)
        return Response(serializer.data)

    def put(self, request, consultation_id, *args, **kwargs):
        serializer = ConsultationUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        consultation = ConsultationService.update_consultation(
            consultation_id, serializer.validated_data
        )
        response_serializer = ConsultationSerializer(consultation)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, consultation_id, *args, **kwargs):
        serializer = ConsultationUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        consultation = ConsultationService.update_consultation(
            consultation_id, serializer.validated_data
        )
        response_serializer = ConsultationSerializer(consultation)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
