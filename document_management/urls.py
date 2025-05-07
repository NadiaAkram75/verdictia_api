from django.urls import path
from .views import UploadDocumentView, ListProfessionalDocuments, DownloadDocumentView

urlpatterns = [
    path('upload/', UploadDocumentView.as_view(), name='upload'),
    path('received/', ListProfessionalDocuments.as_view(), name='received'),
    path('download/<uuid:doc_id>/', DownloadDocumentView.as_view(), name='download'),
]
