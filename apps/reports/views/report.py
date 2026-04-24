from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reports.serializers import (
    ReportSerializer,
    ReportCreateSerializer,
    ReportUpdateSerializer,
)
from apps.reports.services import ReportService


class ReportListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        reports = ReportService.list_reports()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ReportCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        report = ReportService.create_report(serializer.validated_data)
        response_serializer = ReportSerializer(report)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ReportDetailAPIView(APIView):
    def get(self, request, report_uuid, *args, **kwargs):
        report = ReportService.get_report_by_uuid(report_uuid)
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    def put(self, request, report_uuid, *args, **kwargs):
        serializer = ReportUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        report = ReportService.update_report(report_uuid, serializer.validated_data)
        response_serializer = ReportSerializer(report)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, report_uuid, *args, **kwargs):
        serializer = ReportUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        report = ReportService.update_report(report_uuid, serializer.validated_data)
        response_serializer = ReportSerializer(report)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
