import secrets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tracker.permissions import IsSuperUser, IsOwner, IsCurrentUser
from tracker.services import send_telegram_message
from .models import User
from .serializers import UserSerializer
from rest_framework import generics, status


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
    permission_classes = [IsAuthenticated, IsCurrentUser]
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

    def update(self, request, *args, **kwargs):
        if self.request.data.get('telegram_chat_id'):
            chat_id = self.request.data.get('telegram_chat_id')
            verify_code = 1000 + secrets.randbelow(9000)
            send_telegram_message(chat_id, f'Ваш код верификации: {verify_code}')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(generics.CreateAPIView):
    '''
    Регистрация пользователя
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if self.request.data.get('telegram_chat_id'):
            chat_id = self.request.data.get('telegram_chat_id')
            verify_code = 1000 + secrets.randbelow(9000)
            send_telegram_message(chat_id, f'''Ваш код верификации: {verify_code}
Для подтверждения Telegram ID авторизуйтесь и введите код''')
            user = serializer.save(is_active=True, telegram_code=verify_code)
        else:
            user = serializer.save(is_active=True)
        user.set_password(self.request.data['password'])
        user.save()


class UserVerifyTelegramIDAPIView(generics.UpdateAPIView):
    '''
    Получает от пользователя код верификации и активирует рассылку через телеграм
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.telegram_code == request.data.get('telegram_code'):
            user.telegram_code = None
            user.is_telegram_verified = True
            user.save()
            send_telegram_message(user.telegram_chat_id, 'Уведомления подключены')
            return Response(status=status.HTTP_200_OK)
        send_telegram_message(user.telegram_chat_id, 'Введен неверный код верификации')
        return Response(status=status.HTTP_400_BAD_REQUEST)
