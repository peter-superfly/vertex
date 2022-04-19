from django.contrib import admin
from .models import Space, Room, RoomMembership, SpaceMemberShip

admin.site.register(Space)
admin.site.register(Room)
admin.site.register(RoomMembership)
admin.site.register(SpaceMemberShip)