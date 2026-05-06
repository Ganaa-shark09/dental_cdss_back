from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.documents.serializers import (
    DocumentSerializer,
    DocumentCreateSerializer,
    DocumentUpdateSerializer,
)
from apps.documents.services import DocumentService


class DocumentListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        documents = DocumentService.list_documents()
        serializer = DocumentSerializer(
            documents, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DocumentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document = DocumentService.create_document(serializer.validated_data, request.user)
        response_serializer = DocumentSerializer(document, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class DocumentDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, document_uuid, *args, **kwargs):
        document = DocumentService.get_document_by_uuid(document_uuid)
        serializer = DocumentSerializer(document, context={"request": request})
        return Response(serializer.data)

    def put(self, request, document_uuid, *args, **kwargs):
        serializer = DocumentUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document = DocumentService.update_document(
            document_uuid, serializer.validated_data, request.user
        )
        response_serializer = DocumentSerializer(document, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, document_uuid, *args, **kwargs):
        serializer = DocumentUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        document = DocumentService.update_document(
            document_uuid, serializer.validated_data, request.user
        )
        response_serializer = DocumentSerializer(document, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_200_OK)
