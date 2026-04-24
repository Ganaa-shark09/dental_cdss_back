from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.odontology.serializers import (
    ToothRecordSerializer,
    ToothRecordCreateSerializer,
    ToothRecordUpdateSerializer,
)
from apps.odontology.services import OdontologyService


class ToothRecordListCreateAPIView(APIView):
    def get(self, request, chart_uuid, *args, **kwargs):
        tooth_records = OdontologyService.list_tooth_records(chart_uuid)
        serializer = ToothRecordSerializer(tooth_records, many=True)
        return Response(serializer.data)

    def post(self, request, chart_uuid, *args, **kwargs):
        serializer = ToothRecordCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tooth_record = OdontologyService.create_tooth_record(
            chart_uuid=chart_uuid,
            validated_data=serializer.validated_data,
        )
        response_serializer = ToothRecordSerializer(tooth_record)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ToothRecordDetailAPIView(APIView):
    def get(self, request, chart_uuid, tooth_record_uuid, *args, **kwargs):
        tooth_record = OdontologyService.get_tooth_record(chart_uuid, tooth_record_uuid)
        serializer = ToothRecordSerializer(tooth_record)
        return Response(serializer.data)

    def put(self, request, chart_uuid, tooth_record_uuid, *args, **kwargs):
        serializer = ToothRecordUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tooth_record = OdontologyService.update_tooth_record(
            chart_uuid,
            tooth_record_uuid,
            serializer.validated_data,
        )
        response_serializer = ToothRecordSerializer(tooth_record)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, chart_uuid, tooth_record_uuid, *args, **kwargs):
        serializer = ToothRecordUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        tooth_record = OdontologyService.update_tooth_record(
            chart_uuid,
            tooth_record_uuid,
            serializer.validated_data,
        )
        response_serializer = ToothRecordSerializer(tooth_record)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
