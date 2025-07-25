from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Habit
from rest_framework import generics, viewsets, status
from .paginators import CustomPagination
from .permissions import IsSuperUser, IsOwner
from .serializers import HabitSerializer
from .services import send_telegram_message, _async_send_telegram_message, sync_send_telegram_message


class HabitsViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для просмотра привычек
    '''
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Habit.objects.filter(owner=self.request.user)
        if self.request.user.is_superuser:
            queryset = Habit.objects.all()
        return queryset


class PublicHabitsAPIView(generics.ListAPIView):
    '''
    APIView для просмотра только публичных привычек
    '''
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination


class TestTGAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    def get(self, *args, **kwargs):
        sync_send_telegram_message('385064001', 'test message')
        return Response(status=status.HTTP_200_OK)
