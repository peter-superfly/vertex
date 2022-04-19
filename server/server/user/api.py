import uuid
import time
import random
import string
import json
import filetype
from urllib.parse import urlparse
from urllib.request import urlopen 
from django.core.files.base import ContentFile
from datetime import datetime
from twilio.rest import Client
from rest_framework import status
from rest_framework import viewsets
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, permissions
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from django.core import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django_otp.oath import totp
from django.utils import timezone

from space.models import Space, Room
from user.models import User, Invitation, UserEmail
from space.serializers import SpaceSerializer, SpaceMemberShipSerializer
from main.settings import EMAIL_FROM, EMAIL_BCC, FRONTEND_URL, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_PHONE_NUMBER, SPACE_NAME
from .serializers import UserSerializer, InvitationSerializer, InviteUserSerializer, EmailSerializer, PasswordResetSerializer, PasswordChangeSerializer, UserEmailSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Q
from django.contrib.auth import password_validation

from utils.utils import generate_otp, randomNumber, randomString, verifyAlphaNumeric

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ObtainTokenPairView(TokenObtainPairView):
    permission_classes  =   (permissions.AllowAny,)
    serializer_class    =   MyTokenObtainPairSerializer

class ConfirmEmail(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        if User.objects.filter( email = request.data.get('email') ).exists():
            currentUser                 =   User.objects.get( email = request.data.get('email') )
            inputVerificationCode       =   request.data.get('verificationCode')
            originVerificationCode      =  generate_otp(currentUser.user_id, 600, 6)
            if originVerificationCode == str(inputVerificationCode):
                currentUser.email_verified = True
                currentUser.save()
                if 'verification_code_detail' in request.session:
                    del request.session["verification_code_detail"]
                token = MyTokenObtainPairSerializer.get_token(currentUser)
                avatar = None
                if currentUser.avatar:
                    avatar = currentUser.avatar.url
                response_data = {
                    "refresh": str(token),
                    "access": str(token.access_token),
                    "user_id": currentUser.user_id,
                    "email": currentUser.email,
                    "fullname": currentUser.fullname,
                    "email_verified": currentUser.email_verified,
                    "avatar": avatar,
                    "success": True
                }
                
                return Response(response_data)
            else:
                return Response({'success': False, 'message':'Not verified, wrong verification code!'})
        else:
            return Response({'success': False, 'message':'No such email address!'})

class ResendOtp(APIView):
    throttle_scope     = 'resendotp'
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        if User.objects.filter( email = request.data.get('email') ).exists():
            currentUser                 =   User.objects.get( email = request.data.get('email') )
            verificationCode            =   generate_otp(currentUser.user_id, 600, 6)
            emailTo         =    currentUser.email
            subjectForEmail =   '🎈 Resend verification code from Skyspace'
            text_mail_body  =   'Hi, ' + currentUser.fullname + '. Your verification code is : ' + verificationCode + ''
            template        =   get_template('mails/register.html')
            html_mail_body  =   template.render({'name': currentUser.fullname, 'email': emailTo, 'code': verificationCode})
            
            msg = EmailMultiAlternatives(subject=subjectForEmail, from_email=EMAIL_FROM, to=[emailTo], bcc=[EMAIL_BCC], body=text_mail_body)
            msg.attach_alternative(html_mail_body, "text/html")
            msg.send()
            
            now = time.time()
            verification_code_detail = {
                "created_time": now,
                "expire_in_seconds": 600,
                "resend_code_in": 60
            }
            request.session["verification_code_detail"] = verification_code_detail
            return Response({'success': True})
        else:
            return Response({'success': False, 'message':'No such email address!'})
            
            
class SecondaryEmailResendOtp(APIView):
    
    throttle_scope     = 'resendotp'

    def post(self, request, format='json'):
        if UserEmail.objects.filter( email = request.data.get('email') ).exists():
            currentUser     =   request.user
            verificationCode=   generate_otp(currentUser.user_id, 600, 6)
            emailTo         =    request.data.get('email')
            subjectForEmail =   '🎈 Resend verification code from Skyspace'
            text_mail_body  =   'Hi, ' + currentUser.fullname + '. Your verification code is : ' + verificationCode + ''
            template        = get_template('mails/code_verify.html')
            header_message  = 'New Email Added'
            html_mail_body  = template.render({'name': request.user.fullname,'email':emailTo,'code':verificationCode,"header":header_message})
            msg = EmailMultiAlternatives(subject=subjectForEmail, from_email=EMAIL_FROM, to=[emailTo], bcc=[EMAIL_BCC], body=text_mail_body)
            msg.attach_alternative(html_mail_body, "text/html")
            msg.send()
            
            now = time.time()
            verification_code_detail = {
                "created_time": now,
                "expire_in_seconds": 600,
                "resend_code_in": 60
            }
            request.session["verification_code_detail"] = verification_code_detail
            return Response({'success': True})
        else:
            return Response({'success': False, 'message':'No such email address!'})


class Register(APIView):
    
    """ User registration functionality. This class is used to create new user.
    
    args: Json body:  Required field {email, fullname, password}
    
    response: Json: User detail  """
    
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        try:
            email      = request.data.get('email').lower()
            full_name  = request.data.get('fullname')
            password   = request.data.get('password')
        except:
            return Response({"message": "Please provide valid data", "required field": "email, fullname, password" }, status=status.HTTP_400_BAD_REQUEST)
            
        # Check user is exist!
        if User.objects.filter( email__iexact = email ):
            return Response( { "message" : "You account already exists" , "status_code":409} )
             
        else:
            requestData = {
                "username": email,
                "email": email,
                "password": password,
                "fullname": full_name,
                "email_verified": True
            }
            
            serializer  = UserSerializer( data = requestData )
            if serializer.is_valid():
                user = serializer.save()
                space = Space.objects.get(space_name=SPACE_NAME)
                space_membership_data = {
                    "user": user.user_id,
                    "space": space.id,
                    "invitor": space.owner.user_id
                }
                spaceMemberShipSerializer = SpaceMemberShipSerializer(data = space_membership_data)
                if spaceMemberShipSerializer.is_valid():
                    spaceMemberShipSerializer.save()
                    space.members.add(user)
               
                if user:
                    json = { "user" : serializer.data }
                    verificationCode = generate_otp(user.user_id, 600, 6)
                    emailTo          =    user.email
                    subjectForEmail  =   '🎈 Welcome to Skyspace!  Confirm You Email'
                    text_mail_body   =   'Hi, ' + user.fullname + '. Your verification code is : ' + verificationCode + ''
                    template         =   get_template('mails/register.html')
                    html_mail_body   =   template.render({'name': user.fullname, 'email': emailTo, 'code': verificationCode})
                    
                    msg = EmailMultiAlternatives(subject=subjectForEmail, from_email=EMAIL_FROM, to=[emailTo], bcc=[EMAIL_BCC], body=text_mail_body)
                    msg.attach_alternative(html_mail_body, "text/html")
                    #msg.send()
                    now  = time.time()
                    verification_code_detail = {"created_time": now,"expire_in_seconds": 600,"resend_code_in": 60}
                    request.session["verification_code_detail"] = verification_code_detail
                    code_expire_detail = { "is_code_expired": False, "code_expire_in": 600, "allow_resend_code": False , "code_resend_in":60}
                    json["code_expire_detail"] = code_expire_detail
                    return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
                    
    serializer_class = UserSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        return User.objects.filter(user_id = self.request.user.user_id)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        payload = {
            "fullname": request.data.get("fullname"),
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
        }
        serializer = self.get_serializer(instance, data=payload, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return self.update(request, *args, **kwargs)


class PasswordResetEmailView(viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EmailSerializer

    def send(self, request):
        return_response = {
            "status": False,
            "message": ""
        }
        try:
            serializer = self.get_serializer_class()(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = get_object_or_404(User, email=serializer.data['email'])
            if user:
                reset_token = FRONTEND_URL + "user/reset-password/?oobCode=" + PasswordResetTokenGenerator().make_token(user=user) + '_' + str(user.pk)
                emailsTo        = user.email
                subjectForEmail = '🎈Skyspace Support - Reset your password.'
                text_mail_body  = 'Hi, ' + user.fullname + ' Please use this link to reset your password. Link:' + reset_token
                template        = get_template('mails/password_reset.html')
                html_mail_body  = template.render({'name': user.fullname, 'link':reset_token})
                
                msg = EmailMultiAlternatives(subject=subjectForEmail, from_email=EMAIL_FROM, to=[emailsTo], bcc=[EMAIL_BCC], body=text_mail_body)
                msg.attach_alternative(html_mail_body, "text/html")
                msg.send()
                return_response["status"] = True
                return_response["message"] = "Password reset link has been sent on your email."
            else:
                return_response["message"] = "An account with that email does not exist."
        except:
            return_response["message"] = "Bad request."
       
        return Response(return_response)

class PasswordResetView(viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordResetSerializer

    def reset(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(user_id=serializer.validated_data.get('user_id'))
        user.set_password(serializer.validated_data.get('new_password'))
        user.save()
        token = MyTokenObtainPairSerializer.get_token(user)
        avatar = None
        if user.avatar:
            avatar = user.avatar.url
        response_data = {
            "refresh": str(token),
            "access": str(token.access_token),
            "user_id": user.user_id,
            "email": user.email,
            "fullname": user.fullname,
            "email_verified": user.email_verified,
            "avatar": avatar,
            "success": True,
        }
       
        return Response(response_data, status=status.HTTP_200_OK)

class PasswordChangeView(viewsets.GenericViewSet):

    serializer_class = PasswordChangeSerializer
   
    def reset(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.check_password(serializer.validated_data.get('old_password')):
            request.user.set_password(serializer.validated_data.get('new_password'))
            request.user.save()
            
            emailTo         =    request.user.email
            subjectForEmail =   '🎈 Your Password has been changed.'
            text_mail_body  =   'Hi, ' + request.user.fullname + '. Your password for signing in to Skyspace Live was recently changed. If you made this change, then we are all set.'
            template        =   get_template('mails/change_password.html')
            html_mail_body  =   template.render({'name': request.user.fullname})
            
            msg = EmailMultiAlternatives(subject=subjectForEmail, from_email=EMAIL_FROM, to=[emailTo], bcc=[EMAIL_BCC], body=text_mail_body)
            msg.attach_alternative(html_mail_body, "text/html")
            msg.send()
            
            return Response({"message": "Your Password has been changed."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Your current password is missing or incorrect; it's required to change the Password."}, status=status.HTTP_400_BAD_REQUEST)


class UserEmailViewSet(viewsets.GenericViewSet):
    
    """ This class is used to perform CRUD operation on UserEmail models."""
    
    def create(self, request):
        if User.objects.filter( email__iexact = request.data.get('email')):
            return Response( { "message" : "This email already taken" , "status_code":409} )
        
        request.data["user"] = request.user.user_id
        serializer = UserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = UserEmail.objects.create(email=serializer.validated_data.get('email'), user=request.user)
        user_email.save()
        verificationCode = generate_otp(request.user.user_id, 600, 6)
        emailTo         = user_email.email
        subjectForEmail = '🎈Email Added.'
        text_mail_body  = 'Hi, ' + request.user.fullname + 'Please use code to confirm your email. Code: '+verificationCode+''
        template        = get_template('mails/code_verify.html')
        header_message  = 'New Email Added'
        html_mail_body  = template.render({'name': request.user.fullname,'email':emailTo,'code':verificationCode,"header":header_message})
        
        msg = EmailMultiAlternatives(subject=subjectForEmail, from_email=EMAIL_FROM, to=[emailTo], bcc=[EMAIL_BCC], body=text_mail_body)
        msg.attach_alternative(html_mail_body, "text/html")
        msg.send()
        
        return Response({"emails": serializer.data, "message": "Email added successfully"}, status=status.HTTP_201_CREATED)
        
    def lists(self, request):
        queryset = UserEmail.objects.filter(user=request.user)
        serializer = UserEmailSerializer(queryset, many=True)
        response_data = { "secondary_emails" : serializer.data, "primary_email": request.user.email }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def destroy(self, request, id=None):
        userEmail = get_object_or_404(UserEmail,id=id)
        if userEmail:
            userEmail.delete()
        return Response({"message": "Email deleted successfully"})
        
        
class ConfirmSecondaryEmail(APIView):
   
    def post(self, request, format='json'):
        return_value = {
            "status": False,
            "message": ''
        }
        if UserEmail.objects.filter( email = request.data.get('email') ).exists():
            inputVerificationCode       =   request.data.get('verificationCode')
            originVerificationCode      =   generate_otp(request.user.user_id, 600, 6)
            if originVerificationCode == str(inputVerificationCode):
                userEmail = UserEmail.objects.get(email=request.data.get('email'))
                userEmail.email_verified = True
                userEmail.save()
                emailsTo = []
                user_emails = UserEmail.objects.filter(email_verified = True, user=request.user )
                for user_email in user_emails:
                    emailsTo.append(user_email.email)
                emailsTo.append(request.user.email)
                subjectForEmail = '🎈Email Added.'
                text_mail_body  = 'Hi, ' + request.user.fullname + ' New email is added to your account'
                template        = get_template('mails/message.html')
                header_message  = 'New email has been added to your account' 
                html_mail_body  = template.render({'name': request.user.fullname, 'header':header_message})
                
                msg = EmailMultiAlternatives(subject=subjectForEmail, from_email=EMAIL_FROM, to=emailsTo, bcc=[EMAIL_BCC], body=text_mail_body)
                msg.attach_alternative(html_mail_body, "text/html")
                msg.send()
                
                return_value["status"] = True
                return_value["message"] = 'Email verified successfully.'
            else:
                return_value["status"] = False
                return_value["message"] = 'Not verified, wrong verification code!'
        else:
            return_value["status"] = False
            return_value["message"] = 'No such email address!'
           
        return Response(return_value)


class OtpExpireTimer(APIView):
    
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, format='json'):
        is_code_expired = True
        allow_resend_code = True
        code_expire_in = 0
        code_resend_in = 0
        try:
            if 'verification_code_detail' in request.session:
                code_detail  = request.session["verification_code_detail"]
                created_time = code_detail["created_time"]
                expire_time  = code_detail['expire_in_seconds']
                resend_time  = code_detail['resend_code_in']
                now = time.time()
                duration = now - created_time
                if duration < expire_time:
                    code_expire_in = int(expire_time - duration)
                    is_code_expired = False
                if duration < code_detail['resend_code_in']:
                    allow_resend_code = False
                    code_resend_in = int(resend_time - duration)
        except:
            pass     
        return Response({ "is_code_expired": is_code_expired, "code_expire_in": code_expire_in, "allow_resend_code": allow_resend_code , "code_resend_in":code_resend_in })


class GetSpaceName(APIView):
    
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, format='json'):
        return_value = {
            "status_code": 200,
            "message": None,
            "data":[]
        }
        
        fullname = request.GET["fullname"]
        space_name = request.GET["space_name"]
        # Check if input is valid:
        if verifyAlphaNumeric(space_name):
            if Space.objects.filter(space_name=space_name).exists():
                spaceName =  f'{space_name}_{randomString(2)}{randomNumber(3)}'
                spaceNames = []
                while len(spaceNames) < 5:
                    if Space.objects.filter(space_name=spaceName).exists():
                        if verifyAlphaNumeric(fullname):
                            spaceName =  f'{fullname}_{randomString(2)}{randomNumber(3)}'
                        else:
                            spaceName =  f'{randomString(5)}_{randomNumber(3)}'
                    else:
                        spaceNames.append({"space_name": spaceName})
                        if verifyAlphaNumeric(fullname):
                            spaceName =  f'{fullname}_{randomString(2)}{randomNumber(3)}'
                        else:
                            spaceName =  f'{randomString(5)}_{randomNumber(3)}'
                    return_value["message"] = "Space Name already taken!"
                    return_value["status_code"] = 409
                    return_value["data"] = spaceNames
            else:
                return_value["message"] = "Valid"
                return_value["data"] = [{"space_name": space_name}]
        else:
            return_value["message"] = "Invalid space name"
        return Response(return_value)


class UploadAvatar(APIView):
    """ This class is used to update user profile image. """
    
    def post(self, request):
        return_value = {
            "status": False,
            "message": None,
            "avatar": None
        }
        try:
            avatar_type = str(request.data.get('avatar_type'))
            valid_image_extensions = ['jpg','jpeg', 'png', 'gif']
            image_name = ''
            image = None
            is_request_valid = True
            if avatar_type and avatar_type == "image":
                image = request.FILES["avatar"]
                image_name = image.name
            elif avatar_type and avatar_type == "url":
                try:
                    img_url = request.data.get('img_url')
                    parsed_img_url = urlparse(img_url)
                    image_name = parsed_img_url.path.split('/')[-1]
                    image = ContentFile(urlopen(img_url).read())
                except:
                    is_request_valid = False
                    return_value["message"] = "Invalid image url!"
            else:
                is_request_valid = False
                return_value["message"] = "Field required avatar_type. accepted : image/url"
            if is_request_valid:
                extension = filetype.guess(image).extension
                if extension not in valid_image_extensions:
                    return_value["message"] = "invalid file format! except: jpg, jpeg, png, gif"
                elif image.size > 5242880:
                    return_value["message"] = "Uploaded image is too large. The maximum file size accepted is 5MB"
                else:
                    user = User.objects.get(user_id=request.user.user_id)
                    user.avatar.save(image_name, image, save=True)
                    return_value["message"] = "Success"
                    return_value["status"] = True
                    return_value["avatar"] = str(user.avatar.url)
        except:
            return_value["message"] = "Something is wrong!"

        return Response(return_value)
        
        
class SearchView(APIView):
    """ This class is use to search user, space, room 
        Method: Post
        Body: (Json) {"search_type, search_text}
        Response: Json List of data     """
    
    def post(self, request):
        try:
            search_type = request.data.get("search_type")
            seacrh_text = request.data.get("search_text")
            return_value = None
            message = 'Success'
            if search_type == "user":
                return_value = User.objects.filter(
                    Q(fullname__icontains=seacrh_text) | 
                    Q(username__icontains=seacrh_text) | 
                    Q(email__icontains=seacrh_text)).exclude(user_id=request.user.user_id)[:5].values('fullname', "user_id", "email", "username", "avatar")
            elif search_type == "space":
                return_value = Space.objects.filter(Q(space_name__icontains=seacrh_text) | Q(display_name__icontains=seacrh_text))[:5].values('id', "display_name", "space_name")
            elif search_type == "room":
                return_value = Room.objects.filter(Q(display_name__icontains=seacrh_text))[:5].values('id', "display_name")
            else:
                message = "Invalid search_type, Available Options: user, space, room"
        except:
            message = "Bad request"    
        
        return Response({"message": message ,"data":return_value})