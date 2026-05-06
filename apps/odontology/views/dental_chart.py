from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.odontology.serializers import (
    DentalChartSerializer,
    DentalChartCreateSerializer,
    DentalChartUpdateSerializer,
)
from apps.odontology.services import OdontologyService


class DentalChartListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        charts = OdontologyService.list_charts()
        serializer = DentalChartSerializer(charts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DentalChartCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chart = OdontologyService.create_chart(serializer.validated_data, request.user)
        response_serializer = DentalChartSerializer(chart)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class DentalChartDetailAPIView(APIView):
    def get(self, request, chart_uuid, *args, **kwargs):
        chart = OdontologyService.get_chart_by_uuid(chart_uuid)
        serializer = DentalChartSerializer(chart)
        return Response(serializer.data)

    def put(self, request, chart_uuid, *args, **kwargs):
        serializer = DentalChartUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chart = OdontologyService.update_chart(chart_uuid, serializer.validated_data, request.user)
        response_serializer = DentalChartSerializer(chart)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, chart_uuid, *args, **kwargs):
        serializer = DentalChartUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        chart = OdontologyService.update_chart(chart_uuid, serializer.validated_data, request.user)
        response_serializer = DentalChartSerializer(chart)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
