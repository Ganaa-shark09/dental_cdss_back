from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cdss.serializers import CdssEngineSerializer
from apps.cdss.services import CdssService


class CdssEngineListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cdss_engines = CdssService.list_cdss_engines()
        serializer = CdssEngineSerializer(cdss_engines, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        consultation_id = request.data.get("consultation_id")
        consultation = CdssService.get_consultation(consultation_id)
        cdss_engine = CdssService.analyze_consultation(consultation)

        serializer = CdssEngineSerializer(cdss_engine)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CdssEngineDetailAPIView(APIView):
    def get(self, request, cdss_engine_id, *args, **kwargs):
        cdss_engine = CdssService.get_cdss_engine_by_id(cdss_engine_id)
        serializer = CdssEngineSerializer(cdss_engine)
        return Response(serializer.data)
