from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cdss.serializers import CdssEngineSerializer, CdssEngineUpdateSerializer
from apps.cdss.services import CdssService


class CdssEngineListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cdss_engines = CdssService.list_cdss_engines()
        serializer = CdssEngineSerializer(cdss_engines, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        consultation_id = request.data.get("consultation_id")
        if not consultation_id:
            return Response(
                {"consultation_id": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        consultation = CdssService.get_consultation(consultation_id)
        cdss_engine = CdssService.analyze_consultation(consultation)

        serializer = CdssEngineSerializer(cdss_engine)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CdssEngineDetailAPIView(APIView):
    def get(self, request, cdss_engine_uuid, *args, **kwargs):
        cdss_engine = CdssService.get_cdss_engine_by_uuid(cdss_engine_uuid)
        serializer = CdssEngineSerializer(cdss_engine)
        return Response(serializer.data)

    def put(self, request, cdss_engine_uuid, *args, **kwargs):
        serializer = CdssEngineUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cdss_engine = CdssService.update_cdss_engine(
            cdss_engine_uuid, serializer.validated_data
        )
        response_serializer = CdssEngineSerializer(cdss_engine)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, cdss_engine_uuid, *args, **kwargs):
        serializer = CdssEngineUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        cdss_engine = CdssService.update_cdss_engine(
            cdss_engine_uuid, serializer.validated_data
        )
        response_serializer = CdssEngineSerializer(cdss_engine)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
