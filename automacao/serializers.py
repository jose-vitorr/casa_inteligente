from dataclasses import fields
from rest_framework import serializers
from .models import House, Room, Device, Scene, SceneAction

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class SceneActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneAction
        fields = '__all__'


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = '__all__'

    