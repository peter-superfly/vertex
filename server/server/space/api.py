import uuid
import time;
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.core import serializers
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, views, generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import PageNumberPagination

from main.settings import EMAIL_FROM, EMAIL_BCC, FRONTEND_URL

from utils.utils import generate_otp, randomNumber, randomString, verifyAlphaNumeric, random_img

from .serializers import (
    RoomSerializer,
    RoomListSerializer,
    SpaceSerializer,
    SpaceMemberShipSerializer,
    RoomMemberShipSerializer,
    RoomListSerializer)
    
from user.serializers import UserSerializer

from .models import (
        Room, Space, SpaceMemberShip, RoomMembership, SpaceMembershipStatus, SpaceMembershipType, RoomMembershipStatus, RoomMembershipType
    )

from user.models import User, Invitation

class ListPagination(PageNumberPagination):
    page_size = 10

# Room viewset
class RoomViewSet(viewsets.ModelViewSet):
    
    """ The Room functionality, This class is use to handle the CRUD opration on Room Model by implimenting some internal logic. """
    
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.filter(Q(owner = self.request.user.user_id) | Q(members__in=[self.request.user]))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
    def retrieve(self, request, *args, **kwargs):
        instance = Room.objects.get(id=kwargs["pk"])
        serializer = RoomListSerializer(instance)
        return Response(serializer.data)  
    
    
    def create(self, request, format='json'):
        message = ''
        errors = ''
        data = None
        response_status = status.HTTP_200_OK
        request.data["owner"] = request.user.user_id
        request.data["members"] = [request.user.user_id]
        if 'is_active' not in request.data:
            request.data["is_active"] = True
        if 'thumb_url' not in request.data:
            request.data["thumb_url"] = 'https://www.wonderopolis.org/wp-content/uploads//2014/03/dreamstime_xl_30482329-custom.jpg'
        serializer = RoomSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            room = Room.objects.get(id=data["id"])
            RoomMembership.objects.create(room=room, user=request.user, invitor=request.user, membership_type="ADMIN")
            message = "Success"
            response_status = status.HTTP_201_CREATED
            
        else:
            message = 'Invalid request.'
            errors = serializer.errors
            response_status = status.HTTP_400_BAD_REQUEST

        return Response({ "message": message, "errors": errors, "data": data }, status = response_status)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = Room.objects.get(id=kwargs["pk"])
        if 'id' in request.data or  'is_deleted' in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
   
    def destroy(self, request, *args, **kwargs):
        success = True
        status_code = status.HTTP_200_OK
        try:
            room = self.get_object()
            room.is_deleted = True
            room.save()
            status_code = status.HTTP_204_NO_CONTENT
        except:
            success = False
            status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        return Response({ "success": success }, status=status_code)


class RoomMembers(APIView):
    
    def get(self, request, id):
        status_code = status.HTTP_200_OK
        message = 'Success'
        success = True
        room = None
        members = []
       
        try:
            room = Room.objects.get(id = id)
        except:
            message = "This room does not exist."
            status_code = status.HTTP_404_NOT_FOUND
            return Response({ "message": message, "success": False, "members": members }, status = status_code)
        
        memberships = RoomMembership.objects.filter(Q(room=room) & (Q(user = request.user.user_id) | Q(invitor = request.user.user_id)))
        for membership in memberships:
            user = membership.user
            __membership = RoomMemberShipSerializer(membership).data
            __user = UserSerializer(user).data
            __user["membership"] = __membership
            members.append(__user)
            
        return Response({ "message": message, "success": success, "members": members }, status = status_code)
        
    
    def post(self, request, id):
        users_list  = request.data.get('users_list')
        status_code = status.HTTP_200_OK
        success     = True
        failed      = {}
        message     = "Success"
        room       = None
        
        try:
            room  = Room.objects.get(id = id , owner = request.user.user_id)
        except:
            message = "Unauthorized. You don't have permission to manage this room."
            status_code = status.HTTP_404_NOT_FOUND
            return Response({ "message": message, "success": False, "failed": failed }, status = status_code)
            
        if isinstance(users_list, list):
            for user_list in users_list:
                try:
                    user = User.objects.get(user_id = user_list["user_id"])
                    user_list["user"] = user.user_id
                    user_list["room"] = room.id
                    user_list["invitor"] = request.user.user_id
                    serializer = RoomMemberShipSerializer(data = user_list)
                    if serializer.is_valid():
                        serializer.save()
                        room.members.add(user)
                        room.save()
                        
                    else:
                        failed[user_list["user_id"]] = serializer.errors
                except:
                    failed[user_list["user_id"]] = "This user does not exist."
        else:
            success = False
            message = "Invalid request."
            status_code = status.HTTP_400_BAD_REQUEST
                
        return Response({ "message": message, "success": success, "failed": failed }, status = status_code)
    
    def delete(self, request, id):
        member_ids  = request.data.get('member_ids')
        status_code = status.HTTP_200_OK
        success     = True
        message     = "Success"
        failed      = {}
        room      = None
        try:
            room = Room.objects.get(id = id, owner = request.user.user_id)
        except:
            message = "Unauthorized. You don't have permission to manage this room."
            status_code = status.HTTP_404_NOT_FOUND
            return Response({ "message": message, "success": False}, status = status_code)
            
        if isinstance(member_ids, list):
            for member_id in member_ids:
                try:
                    membership = RoomMembership.objects.get(room = room.id, user = member_id)
                    membership.delete()
                except:
                    failed[member_id] = "This member does not exist"
        else:
            message = "Invalid request."
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
          
        return Response({ "message": message, "success": success, "failed": failed }, status = status_code)
       
        
class InviteUserInRoom(APIView):
    
    def post(self, request):
        user = None
        message = None
        response_status = status.HTTP_200_OK
        room_link = request.data.get("room_link")
        room_name = request.data.get("room_name")
        try:
            user = User.objects.get(user_id=request.data.get("user_id"))
        except:
            response_status = status.HTTP_404_NOT_FOUND
            message = "User not found with the provided user id."
        if user:  
            emailsTo        = user.email
            subjectForEmail = '🎈Skyspace Invitation.'
            text_mail_body  = f'Hi, {user.fullname} You have been invited to the skyspace  {room_name} room please click on link join meeting. {room_link}'
            template        = get_template('mails/notification.html')
            header_message  = 'Join the meeting'
            body_text       = f'You have been invited to the skyspace  {room_name} room please click on button to join meeting.'
            button_text     = 'Join Now'
            html_mail_body  = template.render({'name': user.fullname, 'header_message':header_message, 'body_text':body_text, 'button_text':button_text, 'link':room_link})
            
            msg = EmailMultiAlternatives(subject=subjectForEmail, from_email=EMAIL_FROM, to=[emailsTo], bcc=[EMAIL_BCC], body=text_mail_body)
            msg.attach_alternative(html_mail_body, "text/html")
            msg.send()
            message = "Success"
            
        return Response({"message": message}, status=response_status)

class SpaceMembers(APIView):
    
    def get(self, request, id):
        status_code = status.HTTP_200_OK
        message = "Success"
        success = True
        space = None
        members = []
      
        try:
            space = Space.objects.get(id = id)
        except:
            message = "Unauthorized. You don't have permission to manage this space."
            response_status = status.HTTP_404_NOT_FOUND
            return Response({ "message": message, "success": False, "members": members }, status = status_code)
            
        memberships = SpaceMemberShip.objects.filter(Q(space=space) & Q(user = request.user.user_id) | Q(invitor = request.user.user_id))
        for membership in memberships:
            user = membership.user
            __membership = SpaceMemberShipSerializer(membership).data
            __user = UserSerializer(user).data
            __user["membership"] = __membership
            members.append(__user)
            
        return Response({ "message": message, "success": success, "members": members }, status = status_code)
        
        
    def post(self, request, id):
        users_list  = request.data.get('users_list')
        status_code = status.HTTP_200_OK
        success     = True
        message     = "Success"
        space       = None
        failed      = {}
            
        try:
            space  = Space.objects.get(id = id , owner = request.user.user_id)
        except:
            message = "Unauthorized. You don't have permission to add members to this space"
            status_code = status.HTTP_404_NOT_FOUND
            return Response({ "message": message, "success": False, "failed": failed }, status = status_code)
            
        if isinstance(users_list, list):
            for user_list in users_list:
                try:
                    user = User.objects.get(user_id = user_list["user_id"])
                    user_list["user"] = user.user_id
                    user_list["space"] = space.id
                    user_list["invitor"] = request.user.user_id
                    serializer = SpaceMemberShipSerializer(data = user_list)
                    if serializer.is_valid():
                        serializer.save()
                        space.members.add(user)
                        space.save()
                        member_room_obj = {
                            "space": space.id,
                            "owner": user.user_id,
                            "members": [user.user_id],
                            "display_name": "Common Room",
                            "room_id": f'{user.fullname}_room_{randomNumber(4)}',
                            "description": f'{user.fullname} private room',
                            "thumb_url": "https://www.wonderopolis.org/wp-content/uploads//2014/03/dreamstime_xl_30482329-custom.jpg"
                        }
                        member_room = RoomSerializer(data = member_room_obj)
                        if member_room.is_valid():
                            member_room.save()
                    else:
                        failed[user_list["user_id"]] = serializer.errors
                except:
                    failed[user_list["user_id"]] = "This user does not exist."
        else:
            message = "Invalid request."
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
       
        return Response({ "message": message, "success": success, "failed": failed }, status = status_code)
            
    def delete(self, request, id):
        member_ids  = request.data.get('member_ids')
        status_code = status.HTTP_200_OK
        success     = True
        message     = "Success"
        failed      = {}
        space       = None
        
        try:
            space = Space.objects.get(id = id, owner = request.user.user_id)
        except:
            message = "Unauthorized. You don't have permission to manage this space."
            status_code = status.HTTP_404_NOT_FOUND
            return Response({ "message": message, "success": False}, status = status_code)
            
        if isinstance(member_ids, list):
            for member_id in member_ids:
                try:
                    membership = SpaceMemberShip.objects.get(space = space.id, user = member_id)
                    membership.delete()
                    member = User.objects.get(user_id = member_id)
                    space.members.remove(member)
                    space.save()
                except:
                    failed[member_id] = "This member does not exist"
        else:
            message = "Invalid request."
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
          
        return Response({ "message": message, "success": success, "failed": failed }, status = status_code)


# Space viewset

class SpaceViewSet(viewsets.ModelViewSet):
    
    """
    The Space functionality, This class is use to handle the CRUD opration on Space Model by implimenting some internal logic.
    
    """
    serializer_class = SpaceSerializer
    def get_queryset(self):
        duration_filter = timezone.now() - timezone.timedelta(days=3)
        queryset = Space.objects.filter(Q(members__in=[self.request.user]) & (Q(deleted_at__gte=duration_filter) | Q(deleted_at=None) | Q(is_deleted=False)))
        return queryset
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):

        if Space.objects.filter(space_name=request.data.get("space_name")).count() > 0:
            return Response( { "message" : "Space already exists", "status_code": 409 } )

        space = Space.create(space_name = request.data.get("space_name"), display_name = request.data.get("display_name"), owner=request.user)
        space.save()
        space = Space.objects.get(id=space.id)
        space.members.add(request.user)

        return Response(SpaceSerializer(space).data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
    
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if 'space_name' in request.data or  'is_deleted' in request.data or 'deleted_at' in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
   
    def destroy(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        success = True
        try:
            space = self.get_object()
            if 'delete_type' in request.data:
                if(request.data.get("delete_type") == "temporary"):
                    deleted_at = timezone.now()
                else:
                    deleted_at = timezone.now() - timezone.timedelta(days=4)
                space.is_deleted = True
                space.deleted_at = deleted_at
                space.save()
            else:
                success = False
                status_code = status.HTTP_400_BAD_REQUEST
        except:
            success = False
            status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
    
        return Response({ "success": success }, status=status_code)
        
        
class SpaceRestoreAPI(APIView):
    
    """ This class is used to restore space which is deleted before 72 hours ago. """

    def post(self, request, id):
        return_response = {
            "status": False,
            "message": ""
        }
        try:
            duration_filter = timezone.now() - timezone.timedelta(days=3)
            spaces = Space.objects.filter(Q(id = id) & (Q(deleted_at__gte=duration_filter)))
            if spaces:
                for space in spaces:
                    space.is_deleted = False
                    space.save()
                    return_response["status"] = True
                    return_response["message"] = "Space restored successfully."
            else:
                return_response["message"] = "This space does not exist."
        except:
            return_response["message"] = "Bad request."
            
        return Response(return_response)

        
class RoomsBySpaceId(generics.ListAPIView):
    ''' This class is use to return all rooms by space id 
    
    Methods Accepted: GET(Space id as params)
    
    '''
    serializer_class = RoomListSerializer
    pagination_class = ListPagination
    def get_queryset(self):
        queryset = Room.objects.all().filter(
            (Q(space__id = self.kwargs['id']) & Q(members__in=[self.request.user]) & Q(is_deleted = False)) | 
            (Q(space__id = self.kwargs['id']) & Q(is_private = False) & Q(is_deleted = False)))
        return queryset