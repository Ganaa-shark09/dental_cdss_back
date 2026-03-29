from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cdss.serializers import CdssRecommendationSerializer
from apps.cdss.services import CdssService


class CdssRecommendationListAPIView(APIView):
    def get(self, request, cdss_engine_id, *args, **kwargs):
        recommendations = CdssService.get_cdss_engine_by_id(
            cdss_engine_id
        ).recommendations.all()
        serializer = CdssRecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)
