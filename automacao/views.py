from django.shortcuts import render
from rest_framework import viewsets
from .models import House, Room, Device, Scene, SceneAction
from .serializers import HouseSerializer, RoomSerializer, DeviceSerializer, SceneSerializer, SceneActionSerializer

# Create your views here.
class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class SceneViewSet(viewsets.ModelViewSet):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer


class SceneActionViewSet(viewsets.ModelViewSet):
    queryset = SceneAction.objects.all()
    serializer_class = SceneActionSerializer