from django.urls import path

from apps.cdss.views import (
    CdssEngineListCreateAPIView,
    CdssEngineDetailAPIView,
    CdssEnginePrintAPIView,
    CdssSchemaAPIView,
)
from apps.cdss.views.cdss_recommendation import CdssRecommendationListAPIView

urlpatterns = [
    path("schema/", CdssSchemaAPIView.as_view(), name="cdss-schema"),
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
    path(
        "<uuid:cdss_engine_uuid>/print/",
        CdssEnginePrintAPIView.as_view(),
        name="cdss-engine-print",
    ),
]
