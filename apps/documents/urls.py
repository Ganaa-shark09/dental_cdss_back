from django.urls import path
from apps.documents.views.document import (
    DocumentListCreateAPIView,
    DocumentDetailAPIView,
)

urlpatterns = [
    path("", DocumentListCreateAPIView.as_view(), name="document-list-create"),
    path(
        "<uuid:document_id>/", DocumentDetailAPIView.as_view(), name="document-detail"
    ),
]
