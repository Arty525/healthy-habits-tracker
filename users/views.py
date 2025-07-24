from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny

from tracker.permissions import IsSuperUser
from .models import User
from .serializers import UserSerializer
from rest_framework import generics


class UserListAPIView(generics.ListAPIView):
    '''
    Просмотр списка пользователей, только для супер юзера
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    '''
    Просмотр данных пользователя, только для супер юзера
    '''
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = UserSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    '''
    Удалние пользователя, только для супер юзера
    '''
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSuperUser]


class UserUpdateAPIView(generics.UpdateAPIView):
    '''
    Изменение данных пользователя, только для супер юзера
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]


class UserCreateAPIView(generics.CreateAPIView):
    '''
    Регистрация пользователя
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
