import uuid
import json
from django.db import models
from user.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from utils.utils import alphaNumricValidator

class Space(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    space_name = models.CharField(max_length=24, unique=True)
    display_name = models.CharField(max_length=32)
    updated_at = models.DateTimeField(default=timezone.now)
    members = models.ManyToManyField(User, related_name='members')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    is_private = models.BooleanField(default = True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    @classmethod
    def create(cls, *args, **kwargs):
        space = cls(*args, **kwargs)
        # Create a private room accessible by all room members
        room = Room.objects.create(
            owner = space.owner,
            display_name = "Common Room",
            room_id = "common_room",
            description = "An open room for all members of this room",
            space=space,
            thumb_url="https://www.wonderopolis.org/wp-content/uploads//2014/03/dreamstime_xl_30482329-custom.jpg")
        # Add members in room    
        room.members.add(room.owner)
        # Create room membership
        RoomMembership.objects.create(room=room, user=room.owner, invitor=room.owner, membership_type="ADMIN")
        if space.is_private:
            # Create space membership
            SpaceMemberShip.objects.create(space=space, user=space.owner, invitor=space.owner, membership_type="ADMIN")
 
        return space

    def __str__(self):
        
        return json.dumps({
            "id" : str(self.id),
            "space_name" : self.space_name,
            "display_name" : self.display_name,
            "updated_at" : str(self.updated_at)
        })

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=100)
    room_id = models.CharField(validators=[alphaNumricValidator], max_length=30, blank=False, null=False)
    description = models.CharField(max_length=128, null=True)
    thumb_url = models.CharField(max_length=128, null=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=timezone.now)
    members = models.ManyToManyField(User, related_name='roomMembers')
    is_private = models.BooleanField(default=True)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, db_constraint=False, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
        
    class Meta:
        unique_together = ('space', 'room_id')

    def __str__(self):
        return json.dumps({
            "id" : str(self.id),
            "display_name": str(self.display_name),
            "is_active": str(self.is_active),
            "is_private": str(self.is_private),
            "space_name": str(self.space.space_name),
            "space_id": str(self.space.id),
            "owner_name": str(self.owner.fullname)
        }) 

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="")
    updated_at = models.DateTimeField(default=timezone.now)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, db_constraint=False)

class SpaceMembershipStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', _('Active')
    INACTIVE = 'INACTIVE', _('Inactive')
    INVITED = 'INVITED', _('Invited')
    DECLINED = 'DECLINED', _('Decline')

class SpaceMembershipType(models.TextChoices):
    ADMIN = 'ADMIN', _('Admin')
    MEMBER = 'MEMBER', _('Member')

class SpaceMemberShip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    space = models.ForeignKey(Space, related_name='spaceMemberships', on_delete=models.CASCADE, db_constraint=False, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, db_constraint=False, related_name='spaceMembership')
    invite_time_first = models.DateTimeField(default=timezone.now, null=False)
    invite_time_last = models.DateTimeField(default=timezone.now, null=False)
    join_time = models.DateTimeField(null=True)
    deactivate_time = models.DateTimeField(null=True)
    invitor = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='spaceInvitor')
    membership_status = models.CharField(max_length=8, null=False, choices=SpaceMembershipStatus.choices, default=SpaceMembershipStatus.ACTIVE)
    membership_type = models.CharField(max_length=8, null=False, choices=SpaceMembershipType.choices, default=SpaceMembershipType.MEMBER)

    class Meta:
        unique_together = ('space', 'user')

    def __str__(self):
        return json.dumps({
            "id" : str(self.id),
            "space" : str(self.space.id),
            "user" : str(self.user.user_id),
            "membership_status" : self.membership_status,
            "membership_type" : self.membership_type
        })

class RoomMembershipStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', _('Active')
    INACTIVE = 'INACTIVE', _('Inactive')
    INVITED = 'INVITED', _('Invited')
    DECLINED = 'DECLINED', _('Decline')

class RoomMembershipType(models.TextChoices):
    ADMIN = 'ADMIN', _('Admin')
    MEMBER = 'MEMBER', _('Member')

class RoomMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, related_name='roomMemberships', on_delete=models.CASCADE, db_constraint=False, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, db_constraint=False , related_name='roomMembership')
    invite_time_first = models.DateTimeField(default=timezone.now, null=False)
    invite_time_last = models.DateTimeField(default=timezone.now, null=False)
    join_time = models.DateTimeField(null=True)
    deactivate_time = models.DateTimeField(null=True)
    invitor = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='roomInvitor')
    membership_status = models.CharField(max_length=8, null=False,choices=RoomMembershipStatus.choices, default=RoomMembershipStatus.ACTIVE)
    membership_type = models.CharField(max_length=8, null=False, choices=RoomMembershipType.choices, default=RoomMembershipType.MEMBER)

    class Meta:
        unique_together = ('room', 'user')

    def __str__(self):
        return json.dumps({
            "id" : str(self.id),
            "invitor": str(self.invitor.fullname),
            "member": str(self.user.fullname),
            "membership_status" : self.membership_status,
            "membership_type" : self.membership_type,
            "room_id" : str(self.room.id),
            "member_id" : str(self.user.user_id)
        }) 
