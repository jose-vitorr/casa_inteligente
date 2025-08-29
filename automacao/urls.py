from django.urls import path, include
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from .views import HouseViewSet, RoomViewSet, DeviceViewSet, SceneViewSet, SceneActionViewSet

router = DefaultRouter()
router.register(r'houses', HouseViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'scenes', SceneViewSet)
router.register(r'scene-actions', SceneActionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]