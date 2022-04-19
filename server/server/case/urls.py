from rest_framework import routers
from django.urls import path

from .api import (
    CaseDocumentView,
    CaseFileUploadApiView, 
    CaseDocumentScrapApiView, 
    CaseViewSet,
    UploadCases
)

router = routers.DefaultRouter()

router.register('', CaseViewSet, basename='case')

urlpatterns = router.urls
urlpatterns.append(path('list/search/', CaseDocumentView.as_view({'get': 'list'})))
urlpatterns.append(path('file/upload/', CaseFileUploadApiView.as_view()))
urlpatterns.append(path('bulk/upload/', UploadCases.as_view()))
urlpatterns.append(path('file/scrap/', CaseDocumentScrapApiView.as_view()))
