from rest_framework import serializers
from .models import House, Room, Device, Scene, SceneAction


class DeviceSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name', read_only=True) # Acessa o cômodo do dispositivo
    house_name = serializers.CharField(source='room.house.name', read_only=True) # Nome do cômodo

    class Meta:
        model = Device
        fields = ['id', 'name', 'description', 'activated', 'room', 'room_name', 'house_name']

    def validate_name(self, value):
        # Valida se o nome do dispositivo não está vazio
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("O nome do dispositivo deve ter pelo menos 2 caracteres.")
        return value.strip()
    
    def validate(self, data):
        # Validação para evitar nomes duplicados no mesmo cômodo
        room = data.get('room')
        name = data.get('name', '').strip()
        
        instance_id = self.instance.id if self.instance else None
        
        existing_device = Device.objects.filter(room=room, name__iexact=name)
        if instance_id:
            existing_device = existing_device.exclude(id=instance_id)
            
        if existing_device.exists():
            raise serializers.ValidationError({
                'name': f"Já existe um dispositivo chamado '{name}' neste cômodo."
            })
        
        return data

class RoomSerializer(serializers.ModelSerializer):
    devices = serializers.SerializerMethodField()  # Para controlar melhor a serialização
    devices_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'name', 'house', 'devices', 'devices_count']

    def get_devices(self, obj):
        # Retorna dispositivos da sala com informações básicas
        devices = obj.devices.all()
        return DeviceSerializer(devices, many=True, context=self.context).data
    
    def get_devices_count(self, obj):
        # Retorna a quantidade de dispositivos na sala
        return obj.devices.count()
    
    def validate_name(self, value):
        # Valida se o nome do cômodo não está vazio
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("O nome do cômodo deve ter pelo menos 2 caracteres.")
        return value.strip()
    
def validate(self, data):
        # Validação customizada para evitar nomes duplicados na mesma casa
        house = data.get('house')
        name = data.get('name', '').strip()
        
        # Se estamos atualizando, pega o ID atual
        instance_id = self.instance.id if self.instance else None
        
        # Verifica se já existe um cômodo com esse nome na mesma casa
        existing_room = Room.objects.filter(house=house, name__iexact=name)
        if instance_id:
            existing_room = existing_room.exclude(id=instance_id)
        
        if existing_room.exists():
            raise serializers.ValidationError({
                'name': f"Já existe um cômodo chamado '{name}' nesta casa."
            })
        
        return data

class SceneActionSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    room_name = serializers.CharField(source='device.room.name', read_only=True)

    class Meta:
        model = SceneAction
        fields = ['id', 'device', 'device_name', 'room_name', 'interval', 'order', 'newState']

    def validate_interval(self, value):
        # Valida se o intervalo é um número positivo razoável
        if value < 0:
            raise serializers.ValidationError("O intervalo não pode ser negativo.")
        if value > 3600:  # Máximo de 1 hora
            raise serializers.ValidationError("O intervalo não pode ser maior que 3600 segundos (1 hora).")
        return value
    
    def validate_order(self, value):
        # Valida se a ordem é um número positivo
        if value < 1:
            raise serializers.ValidationError("A ordem deve ser um número positivo (começando em 1).")
        return value
    
    def validate(self, data):
        # Validação para garantir que o dispositivo pertence à mesma casa da cena
        scene = data.get('scene')
        device = data.get('device')
        
        if scene and device:
            if device.room.house != scene.house:
                raise serializers.ValidationError({
                    'device': 'O dispositivo deve pertencer à mesma casa da cena.'
                })
        
        return data

class SceneSerializer(serializers.ModelSerializer):
    actions = SceneActionSerializer(many=True, read_only=True) # actions pq é o related_name no model SceneAction
    actions_count = serializers.SerializerMethodField()

    class Meta:
        model = Scene
        fields = ['id', 'name', 'activated', 'house', 'actions', 'actions_count']

    def get_actions_count(self, obj):
        # Retorna a quantidade de ações na cena
        return obj.actions.count()
    
    def validate_name(self, value):
        # Valida se o nome da cena não está vazio
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("O nome da cena deve ter pelo menos 2 caracteres.")
        return value.strip()
    
    def validate(self, data):
        # Validação para evitar nomes duplicados na mesma casa
        house = data.get('house')
        name = data.get('name', '').strip()
        
        instance_id = self.instance.id if self.instance else None
        
        existing_scene = Scene.objects.filter(house=house, name__iexact=name)
        if instance_id:
            existing_scene = existing_scene.exclude(id=instance_id)
            
        if existing_scene.exists():
            raise serializers.ValidationError({
                'name': f"Já existe uma cena chamada '{name}' nesta casa."
            })
        
        return data

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'

    def validate_name(self, value):
        # Valida se o nome da casa não está vazio e tem tamanho mínimo
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("O nome da casa deve ter pelo menos 2 caracteres.")
        return value.strip()
    
    def validate_owner(self, value):
        # Valida se o proprietário não está vazio
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("O nome do proprietário deve ter pelo menos 2 caracteres.")
        return value.strip()