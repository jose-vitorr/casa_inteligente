from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action 
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
    serializer_class = DeviceSerializer # Serializer refinado
    
    @action(detail=True, methods=['post'])
    def set_state(self, request, pk=None):
        """
        Endpoint para definir o estado de um dispositivo (ligar/desligar).
        Espera um JSON no corpo da requisicao com o campo 'activated' (booleano).
        """
        device = self.get_object()
        
        new_state = request.data.get('activated')

        # Validacao: verifica se o valor foi enviado e é um bool
        if new_state is None or not isinstance(new_state, bool):
            return Response({'error': 'O campo "activated" é obrigatório. Ele deve ser um boolean.'}, status=status.HTTP_400_BAD_REQUEST)

        device.activated = new_state
        device.save()

        return Response({'status': 'device toggled', 'new_state': device.activated}, status=status.HTTP_200_OK)


class SceneViewSet(viewsets.ModelViewSet):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer

    # A antiga ação 'activate' agora é 'execute' e tem nova lógica
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """
        Executa uma cena, alterando o estado dos dispositivos associados.
        A cena só pode ser executada se seu campo 'activated' for true.
        """
        scene = self.get_object()

        # CONDIÇÃO: Verifica se a cena está habilitada para ser executada
        if not scene.activated:
            return Response(
                {'status': f'A cena "{scene.name}" está desativada e não pode ser executada.'},
                status=status.HTTP_403_FORBIDDEN # Forbidden é um bom status code aqui
            )

        actions = scene.actions.all()
        
        if not actions:
            return Response(
                {'status': 'A cena não possui ações para executar.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Lógica de execução (a mesma de antes)
        for action_item in actions:
            device = action_item.device
            device.activated = action_item.newState
            device.save()
            # Lembrete: A lógica de 'interval' requer uma solução mais avançada (background tasks)
            # e está sendo ignorada por enquanto.

        return Response(
            {'status': f'Cena "{scene.name}" executada com sucesso.'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['patch'])
    def toggle_activation(self, request, pk=None):
        """
        Alterna o estado de ativação da cena (ativada/desativada).
        """
        scene = self.get_object()
        newSceneState = request.data.get('activated')

        if newSceneState is None or not isinstance(newSceneState, bool):
            return Response({'error': 'O campo "activated" é obrigatório. Ele deve ser um boolean.'}, status=status.HTTP_400_BAD_REQUEST)
        
        scene.activated = newSceneState
        scene.save()
        
        return Response(
            {'status': f'A cena "{scene.name}" agora está {"ativada" if scene.activated else "desativada"}.'},
            status=status.HTTP_200_OK
        )


class SceneActionViewSet(viewsets.ModelViewSet):
    queryset = SceneAction.objects.all()
    serializer_class = SceneActionSerializer