import base64
from django.contrib.auth import authenticate
from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
   
    def has_permission(self, request, view):
        auth_header = request.META['HTTP_AUTHORIZATION']
        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        user = authenticate(username=username, password=password)
        if user:
            return user.is_superuser  
        return False