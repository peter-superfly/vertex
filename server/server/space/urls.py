from rest_framework import routers
from django.urls import path

from .api import (RoomViewSet, SpaceViewSet, SpaceRestoreAPI,
    SpaceMembers,RoomMembers, InviteUserInRoom, RoomsBySpaceId)

router = routers.DefaultRouter()
router.register('rooms', RoomViewSet, basename='rooms')
router.register('spaces', SpaceViewSet, basename='spaces')


urlpatterns = router.urls
urlpatterns.append(path('<str:id>/members/', SpaceMembers.as_view()))
urlpatterns.append(path('restore/<str:id>/', SpaceRestoreAPI.as_view()))
urlpatterns.append(path('rooms/<str:id>/members/', RoomMembers.as_view()))
urlpatterns.append(path('rooms/user/invite', InviteUserInRoom.as_view()))
urlpatterns.append(path('<str:id>/rooms/', RoomsBySpaceId.as_view()))
