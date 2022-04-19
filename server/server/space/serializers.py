from rest_framework import serializers
from space.models import Room, Event, Space, SpaceMemberShip, RoomMembership
from rest_framework.serializers import CharField
from user.serializers import UserSerializer

class RoomMemberShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMembership
        fields = '__all__'

class RoomMemberShipListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = RoomMembership
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomListSerializer(serializers.ModelSerializer):
    roomMemberships = RoomMemberShipListSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class SpaceSerializer(serializers.ModelSerializer):
    owner_id = CharField(source="owner.user_id")
    class Meta:
        model = Space
        fields = '__all__'

class SpaceMemberShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceMemberShip
        fields = '__all__'

