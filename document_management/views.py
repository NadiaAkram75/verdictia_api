from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Document
from .serializers import DocumentUploadSerializer, DocumentSerializer
from django.http import HttpResponse
from .utils import decrypt_file_content

class UploadDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'client':
            return Response({'error': 'Only clients can upload documents'}, status=403)
        serializer = DocumentUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Document uploaded and encrypted successfully'})
        return Response(serializer.errors, status=400)


class ListProfessionalDocuments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'professional':
            return Response({'error': 'Only professionals can view this'}, status=403)
        docs = Document.objects.filter(assigned_to=request.user)
        return Response(DocumentSerializer(docs, many=True).data)


class DownloadDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doc_id):
        try:
            doc = Document.objects.get(id=doc_id, assigned_to=request.user)
            decrypted = decrypt_file_content(doc.file_encrypted)
            response = HttpResponse(decrypted, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{doc.title}.pdf"'
            return response
        except Document.DoesNotExist:
            return Response({'error': 'Document not found or not authorized'}, status=404)
