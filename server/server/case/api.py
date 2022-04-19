import uuid
import re
import filetype
import logging
from django.utils import timezone
from django.db.models import Q
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, views, generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from main.settings import EMAIL_FROM, EMAIL_BCC, FRONTEND_URL, AWS_RECORDING_BUCKET_NAME
from main.permissions import AdminPermission
from utils.utils import (get_random_alphanumeric_string,
                         generate_otp,
                         randomNumber,
                         randomString,
                         verifyAlphaNumeric,
                         random_img,
                         delete_s3_file,
                         map_case_data)
                         
from scripts.scrap_cases import (scrap_case, scrap_kenya_law, upload_document_to_cloud_storage, scrap_file)

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import mimetypes

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from elasticsearch_dsl import TermsFacet, DateHistogramFacet
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import (
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
    FilteringFilterBackend,
    CompoundSearchFilterBackend,
    FacetedSearchFilterBackend,
    SuggesterFilterBackend,
)

from .serializers import (
    CaseDocumentSerializer,
    CaseSerializer,
    PersonSerializer,
    CaseListSerializer
)
from .documents import CaseDocument

from user.serializers import UserSerializer, InvitationSerializer

from .models import (
    Case, Person
)


class CaseDocumentView(DocumentViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    document = CaseDocument
    serializer_class = CaseDocumentSerializer
    lookup_field = 'id'
    page_size = 20
    filter_backends = [
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        FacetedSearchFilterBackend,
    ]

    ordering = ('-updated_at',)
    search_fields = ('title', 'case_number', 'court_name', 'case_name','citation','parties',)
    ordering_fields = {
        'delivery_date': 'delivery_date',
        'updated_at': 'updated_at'
    }
    multi_match_search_field = ('title', 'case_number', 'court_name', 'case_name','citation','parties',)
    
    filter_fields = {
        'case_class': 'case_class.raw',
        'case_action': 'case_action.raw',
        'judges': 'judges.raw',
        'court_name': 'court_name.raw'
    }
    faceted_search_fields = {
        'judges': {
            'field': 'judges.raw',
            'facet': TermsFacet,
            'enabled': True,
        },
        'court_name': {
            'field': 'court_name.raw',
            'facet': TermsFacet,
            'enabled': True,
        },
        'case_class': {
            'field': 'case_class.raw',
            'facet': TermsFacet,
            'enabled': True,
        },
        'case_action': {
            'field': 'case_action.raw',
            'facet': TermsFacet,
            'enabled': True,
        },
        'updated_at': {
            'field': 'updated_at.raw',
            'facet': DateHistogramFacet,
            'options': {
                'calendar_interval': 'year',
            },
            'enabled': True,
        }
    }



class CaseFileUploadApiView(APIView):
   
    def post(self, request, *args, **kwargs):
        return_response = { "status": False,"message": "", "data": None }
        try:
            if("document" in request.FILES):
                document = request.FILES["document"]
                response = upload_document_to_cloud_storage(document, 'file')
                if(response["status"]):
                    return_response["data"] = response
                    return_response["status"] = True
        except Exception as e:
            return_response["message"] = "Bad request!"

        return Response(return_response)

class UploadCases(APIView):
    def post(self, request, *args, **kwargs):
        from_id = int(request.data.get("from_id")) 
        to_id = int(request.data.get("to_id"))
        clear = request.data.get("clear", '')
        if(clear):
            Case.objects.all().delete()
        res = scrap_kenya_law(from_id, to_id)
         
        return Response(res)


class CaseDocumentScrapApiView(APIView):
   
    def post(self, request, *args, **kwargs):
        return_response = { "status": False,"message": "", "data": None }
        try:
            if("document" in request.FILES):
                document = request.FILES["document"]
                response = scrap_file(document)
                if(response["status"]):
                    return_response["data"] = response["data"]
                    return_response["status"] = True
        except Exception as e:
            return_response["message"] = "Bad request!"

        return Response(return_response)


class CaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    serializer_class = CaseSerializer
    queryset = Case.objects.all()
    pagination_class = PageNumberPagination
    page_size = 6
    filter_backends = [DjangoFilterBackend]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title','case_number']
    filterset_fields = ['case_class', 'case_action']
    ordering_fields = ['updated_at']
    ordering = ['-updated_at']
    
    def create(self, request, *args, **kwargs):
        return_response = {"message": "", "errors": "", "data": None}
        response_status = status.HTTP_200_OK
        try:
            document = None
            if("document" in request.FILES):
                document = request.FILES["document"]
            document_url = request.data.get("document_url")
            document_source = "file"
            request.data._mutable = True
            request.data['judges'] = request.data['judges'].split(",")
            request.data['tags'] = request.data['tags'].split(",")
            response_data = upload_document_to_cloud_storage(document, document_source)
            if(response_data["status"]):
                case_data = {
                    "title": request.data.get("title"),
                    "case_number": request.data.get("case_number"),
                    "court_name": request.data.get("court_name"),
                    "case_name": request.data.get("case_name"),
                    "case_class": request.data.get("case_class"),
                    "case_action": request.data.get("case_action"),
                    "citation": request.data.get("citation"),
                    "parties": request.data.get("parties"),
                    "delivery_date": request.data.get("delivery_date"),
                    "tags": request.data.get("tags"),
                    "judges": request.data.get("judges"),
                    "file_id": response_data["google_file"]["id"]
                }
                serializer = CaseSerializer(data = case_data)
                if serializer.is_valid():
                    serializer.save()
                    return_response['message'] = "success"
                    return_response['data'] = serializer.data
                else:
                    return_response['errors'] = serializer.errors
                    return_response['message'] = "failed"
                    response_status = status.HTTP_400_BAD_REQUEST
            else:
                return_response['errors'] = response_data['message']
                return_response['message'] = "failed"
                response_status = status.HTTP_400_BAD_REQUEST

        except Exception as e:
            return_response['errors'] = str(e)
            return_response['message'] = "failed"
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(return_response, status = response_status)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = Case.objects.get(id=kwargs["pk"])
        if 'id' in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.data._mutable = True
        request.data['judges'] = request.data['judges'].split(",")
        request.data['tags'] = request.data['tags'].split(",")
        case_data = {
            "title": request.data.get("title"),
            "case_number": request.data.get("case_number"),
            "court_name": request.data.get("court_name"),
            "case_name": request.data.get("case_name"),
            "case_class": request.data.get("case_class"),
            "case_action": request.data.get("case_action"),
            "citation": request.data.get("citation"),
            "parties": request.data.get("parties"),
            "delivery_date": request.data.get("delivery_date"),
            "tags": request.data.get("tags"),
            "judges": request.data.get("judges"),
        }
        serializer = self.get_serializer(instance, data=case_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)