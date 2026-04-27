from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.consultations.serializers import (
    ToothComplaintSerializer,
    ToothComplaintCreateSerializer,
    ToothComplaintBulkCreateSerializer,
    ToothComplaintUpdateSerializer,
)
from apps.consultations.services import ToothComplaintService


class ToothComplaintListCreateAPIView(APIView):
    """
    GET  /api/v1/consultations/<uuid>/tooth-complaints/
    POST /api/v1/consultations/<uuid>/tooth-complaints/
    """

    def get(self, request, consultation_id, *args, **kwargs):
        complaints = ToothComplaintService.list_tooth_complaints(consultation_id)
        serializer = ToothComplaintSerializer(complaints, many=True)
        return Response(serializer.data)

    def post(self, request, consultation_id, *args, **kwargs):
        serializer = ToothComplaintCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tc = ToothComplaintService.create_tooth_complaint(
            consultation_id, serializer.validated_data
        )
        return Response(ToothComplaintSerializer(tc).data, status=status.HTTP_201_CREATED)


class ToothComplaintBulkAPIView(APIView):
    """
    POST /api/v1/consultations/<uuid>/tooth-complaints/bulk/

    Accepts {"teeth": [{"tooth_number": "16", "complaint_codes": [...], ...}, ...]}
    Upserts all teeth in one request — used by wizard step 3 (Chief Complaint).
    """

    def post(self, request, consultation_id, *args, **kwargs):
        serializer = ToothComplaintBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        results = ToothComplaintService.bulk_create_or_update_tooth_complaints(
            consultation_id, serializer.validated_data["teeth"]
        )
        return Response(
            ToothComplaintSerializer(results, many=True).data,
            status=status.HTTP_201_CREATED,
        )


class ToothComplaintDetailAPIView(APIView):
    """
    GET    /api/v1/consultations/<uuid>/tooth-complaints/<tc_uuid>/
    PATCH  /api/v1/consultations/<uuid>/tooth-complaints/<tc_uuid>/
    DELETE /api/v1/consultations/<uuid>/tooth-complaints/<tc_uuid>/
    """

    def get(self, request, consultation_id, tooth_complaint_id, *args, **kwargs):
        tc = ToothComplaintService.get_tooth_complaint(consultation_id, tooth_complaint_id)
        return Response(ToothComplaintSerializer(tc).data)

    def patch(self, request, consultation_id, tooth_complaint_id, *args, **kwargs):
        serializer = ToothComplaintUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        tc = ToothComplaintService.update_tooth_complaint(
            consultation_id, tooth_complaint_id, serializer.validated_data
        )
        return Response(ToothComplaintSerializer(tc).data)

    def delete(self, request, consultation_id, tooth_complaint_id, *args, **kwargs):
        ToothComplaintService.delete_tooth_complaint(consultation_id, tooth_complaint_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
