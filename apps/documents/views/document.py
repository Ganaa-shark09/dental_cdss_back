from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.documents.serializers import DocumentSerializer, DocumentCreateSerializer
from apps.documents.services import DocumentService
from apps.documents.models import Document


class DocumentListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        documents = DocumentService.list_documents()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DocumentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document = DocumentService.create_document(serializer.validated_data)
        response_serializer = DocumentSerializer(document)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class DocumentDetailAPIView(APIView):
    def get(self, request, document_id, *args, **kwargs):
        try:
            document = Document.objects.get(id=document_id)
            serializer = DocumentSerializer(document)
            return Response(serializer.data)
        except Document.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
