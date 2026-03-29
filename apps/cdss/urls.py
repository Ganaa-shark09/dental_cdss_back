from django.urls import path

from apps.cdss.views import CdssEngineListCreateAPIView, CdssEngineDetailAPIView
from apps.cdss.views.cdss_recommendation import CdssRecommendationListAPIView

urlpatterns = [
    path("", CdssEngineListCreateAPIView.as_view(), name="cdss-engine-list-create"),
    path(
        "<uuid:cdss_engine_id>/",
        CdssEngineDetailAPIView.as_view(),
        name="cdss-engine-detail",
    ),
    path(
        "<uuid:cdss_engine_id>/recommendations/",
        CdssRecommendationListAPIView.as_view(),
        name="cdss-recommendation-list",
    ),
]
