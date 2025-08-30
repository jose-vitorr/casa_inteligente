from django.urls import path, include
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from .views import HouseViewSet, RoomViewSet, DeviceViewSet, SceneViewSet, SceneActionViewSet

router = DefaultRouter()
router.register(r'houses', HouseViewSet, basename='house')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'scenes', SceneViewSet, basename='scene')
router.register(r'scene-actions', SceneActionViewSet, basename='sceneaction')

urlpatterns = [
    path('', include(router.urls)),
]