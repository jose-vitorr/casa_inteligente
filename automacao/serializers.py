from dataclasses import fields
from rest_framework import serializers
from .models import House, Room, Device, Scene, SceneAction



class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'description', 'activated']

class RoomSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True, read_only=True)  # Inclui dispositivos relacionados

    class Meta:
        model = Room
        fields = ['id', 'name', 'house', 'devices']

class SceneActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneAction
        fields = ['id', 'device', 'interval', 'order', 'newState']


class SceneSerializer(serializers.ModelSerializer):
    actions = SceneActionSerializer(many=True, read_only=True) # actions pq é o related_name no model SceneAction

    class Meta:
        model = Scene
        fields = ['id', 'name', 'activated', 'house', 'actions']

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'
    