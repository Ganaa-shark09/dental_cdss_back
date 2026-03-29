from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.odontology.serializers import (
    ToothRecordSerializer,
    ToothRecordCreateSerializer,
)
from apps.odontology.services import OdontologyService


class ToothRecordListCreateAPIView(APIView):
    def get(self, request, chart_id, *args, **kwargs):
        tooth_records = OdontologyService.list_tooth_records(chart_id)
        serializer = ToothRecordSerializer(tooth_records, many=True)
        return Response(serializer.data)

    def post(self, request, chart_id, *args, **kwargs):
        serializer = ToothRecordCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tooth_record = OdontologyService.create_tooth_record(
            chart_id=chart_id,
            validated_data=serializer.validated_data,
        )
        response_serializer = ToothRecordSerializer(tooth_record)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
