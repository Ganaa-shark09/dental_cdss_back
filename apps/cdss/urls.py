from django.urls import path

from apps.cdss.views import CdssEngineListCreateAPIView, CdssEngineDetailAPIView
from apps.cdss.views.cdss_recommendation import CdssRecommendationListAPIView

urlpatterns = [
    path("", CdssEngineListCreateAPIView.as_view(), name="cdss-engine-list-create"),
    path(
        "<uuid:cdss_engine_uuid>/",
        CdssEngineDetailAPIView.as_view(),
        name="cdss-engine-detail",
    ),
    path(
        "<uuid:cdss_engine_uuid>/recommendations/",
        CdssRecommendationListAPIView.as_view(),
        name="cdss-recommendation-list",
    ),
]
