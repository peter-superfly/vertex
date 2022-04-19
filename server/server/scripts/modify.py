import uuid
from user.models import User, Invitation
from space.models import (Space, Room, SpaceMemberShip,
    SpaceMembershipType, SpaceMembershipStatus)
from pprint import pprint
import random
from space.utils import random_img


def assign_room_images():
    for room in Room.objects.all():
        room.thumb_url = random_img()
        print(room.thumb_url)
        room.save()

def set_user_id():
    for user in User.objects.all():
        user.id = False
        user.save()

def delete_rooms_without_space():
    for room in Room.objects.all():
        print(room.space_id)
        if not room.space_id:
            room.delete()

def create_space_memberships():
    for membership in SpaceMemberShip.objects.all():
        membership.delete()
    for space in Space.objects.all():
        print()
        pprint(space)
        print(space.members.count(), space.members.all())

        for member in space.members.all():
            space_membership = SpaceMemberShip.objects.create(
                space = space,
                user = member,
                invitor = member,
                invite_time_first = space.updated_at,
                join_time = space.updated_at,
                invite_time_last = space.updated_at,
                membership_type = SpaceMembershipType.ADMIN,
                membership_status = SpaceMembershipStatus.ACTIVE
            )

def set_invited_space_members():
    for user in User.objects.all():
        print(user.email)
        user.email = user.email.lower()
        user.username = user.username.lower()
        user.save()

    for invitation in Invitation.objects.all():
        space = Space.objects.get(id=invitation.space_id)
        print()
        print(space)
        print(invitation)
        if User.objects.filter(email__iexact=invitation.email).count():
            user = User.objects.get(email__iexact=invitation.email)
            invitor = User.objects.get(email__iexact='peter@skyspace.live')
            invitation.accepted = True
            invitation.accepted_time = user.date_joined
            invitation.save()
            if not SpaceMemberShip.objects.filter(
                    space=space, user=user).count():
                space_membership = SpaceMemberShip.objects.create(
                    space = space,
                    user = user,
                    invitor = invitor,
                    invite_time_first = space.updated_at,
                    join_time = space.updated_at,
                    invite_time_last = space.updated_at,
                    membership_type = SpaceMembershipType.MEMBER,
                    membership_status = SpaceMembershipStatus.ACTIVE
                )

            print(user)


def run():
    # assign_room_images()
    # delete_rooms_without_space()
    # set_user_id()
    set_invited_space_members()

    # create_space_memberships()
