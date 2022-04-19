import uuid
from django.db.models import Q
from main.settings import SPACE_NAME, COMPANY_NAME
from rest_framework import serializers
from user.models import User, Invitation, UserEmail
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import password_validation
from rest_framework.serializers import ValidationError

from space.models import Space, Room, RoomMembership, SpaceMemberShip

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'email', 'avatar', 'fullname')
  
class SpaceMemberShipSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)
    class Meta:
        model = SpaceMemberShip
        fields = '__all__'

class RoomMemberShipSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)
    class Meta:
        model = RoomMembership
        fields = '__all__'   
        
class SpaceSerializer(serializers.ModelSerializer):
    spaceMemberships= SpaceMemberShipSerializer(many=True, read_only=True)
    class Meta:
        model = Space
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    roomMemberships = RoomMemberShipSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(self, validate_data):
        data = super().validate(validate_data)
        space = None
        rooms = None
        try:
            try:
                space = Space.objects.get(space_name=SPACE_NAME, members__in=[self.user])
            except Exception as e:
                raise ValidationError("You don't have permission in this space", code=401)

            rooms = Room.objects.all().filter(
                (Q(space__id = space.id) & Q(members__in=[self.user]) & Q(is_deleted = False)) | 
                (Q(space__id = space.id) & Q(is_private = False) & Q(is_deleted = False)))
        except Exception as e:
            print(e)
            raise ValidationError("You don't have permission in this space", code=401)
        refresh =   self.get_token(self.user)
        data['refresh'] =   str(refresh)
        data['access'] =   str(refresh.access_token)
        data['user_id'] =   self.user.user_id
        data['email'] =   self.user.email
        data['fullname'] =   self.user.fullname
        data['email_verified']  =   self.user.email_verified
        data['space'] = SpaceSerializer(space).data
        data['rooms'] = RoomSerializer(rooms, many=True).data
       
        if self.user.avatar:
            data['avatar'] = self.user.avatar.url
        else:
            data['avatar'] = None
        currentUser =   User.objects.get(
            user_id = self.user.user_id )
        currentUser.save()
        return data


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField( min_length = 8, write_only = True )

    class Meta:
        model = User

        fields = '__all__'

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class InvitationSerializer(serializers.ModelSerializer):
    space_id = serializers.UUIDField()
    invitor_id = serializers.UUIDField()

    class Meta:
        model = Invitation
        fields = '__all__'


class InviteUserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False)
    token = serializers.CharField(required=True)

    def create(self, validated_data):
        del validated_data['token']
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', ]

class BaseSerializer(serializers.Serializer):
    """Base serializer class providing empty implementations of create/update"""

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

class EmailSerializer(BaseSerializer):
    email = serializers.EmailField()

def parse_password_reset_token(token):
    if not re.match(pattern=r'^[a-z0-9]{1,4}-[a-f0-9]{20}_[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', string=token):
        return None, None
    return token.split('_')

class PasswordResetSerializer(BaseSerializer):
    new_password = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        token, user_id = parse_password_reset_token(attrs['token'])
        print(token)
        print(user_id)
        try:
            user = User.objects.get(user_id=user_id)
        except:
            raise ValidationError('Invalid or expired token')

        if not PasswordResetTokenGenerator().check_token(user=user, token=token):
            raise ValidationError('Invalid or expired token')

        password_validation.validate_password(attrs.get('new_password'), self.instance)
        return {'user_id': user_id, **attrs}

class PasswordChangeSerializer(BaseSerializer):
    new_password = serializers.CharField()
    old_password = serializers.CharField()

    def validate(self, attrs):
        password_validation.validate_password(attrs.get('new_password'), self.instance)
        return {**attrs}


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        fields = '__all__'