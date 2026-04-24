from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cdss.serializers import CdssRecommendationSerializer
from apps.cdss.services import CdssService


class CdssRecommendationListAPIView(APIView):
    def get(self, request, cdss_engine_uuid, *args, **kwargs):
        recommendations = CdssService.list_cdss_recommendations(cdss_engine_uuid)
        serializer = CdssRecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)
