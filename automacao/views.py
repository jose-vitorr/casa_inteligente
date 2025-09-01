from django.shortcuts import render
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema
from .models import House, Room, Device, Scene, SceneAction
from .serializers import HouseSerializer, RoomSerializer, DeviceSerializer, SceneActionBulkUpdateSerializer, SceneActivationSerializer, SceneSerializer, SceneActionSerializer, DeviceStateSerializer

# Create your views here.
class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    filterset_fields = ['owner']

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_fields = ['house']


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer # Serializer refinado
    filterset_fields = ['room']
    
    @extend_schema(
        request=DeviceStateSerializer,
        responses={200: DeviceSerializer},
    )
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
    filterset_fields = ['house']

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

    @extend_schema(
        request=SceneActivationSerializer,
        responses={200: SceneSerializer},
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

    @extend_schema(
        request=SceneActionBulkUpdateSerializer(many=True),
        responses={200: SceneSerializer},
    )
    @action(detail=True, methods=['post'])
    def set_scene_actions(self, request, pk=None):
        """
        Atualiza as ações de uma cena.
        """
        scene = self.get_object()

        # Validando o corpo da requisição
        serializer = SceneActionBulkUpdateSerializer(data=request.data, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data

        try:
            # A transação garante que todas as operações sejam executadas ou nenhuma delas
            with transaction.atomic():
                # Deleta todas as ações existentes da cena
                scene.actions.all().delete()

                # Cria as novas ações
                new_actions = []
                for new_action in validated_data:
                    new_actions.append(SceneAction(
                        scene=scene, 
                        device_id=new_action['device_id'],
                        order=new_action['order'],
                        newState=new_action['newState'],
                        interval=new_action['interval']
                        )
                    )

                # Persiste as novas ações
                SceneAction.objects.bulk_create(new_actions)


        except Exception as e:
            # Se qualquer erro ocorrer, a transação é desfeita (rollback)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Retorna a cena atualizada com a nova lista de ações
        updated_scene_serializer = self.get_serializer(scene)
        return Response(updated_scene_serializer.data, status=status.HTTP_201_CREATED)


class SceneActionViewSet(viewsets.ModelViewSet):
    queryset = SceneAction.objects.all()
    serializer_class = SceneActionSerializer
    filterset_fields = ['scene']

