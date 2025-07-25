from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    '''
    Модель пользователя
    '''
    username = None
    email = models.EmailField(unique=True, verbose_name="E-mail")
    first_name = models.CharField(
        max_length=50, verbose_name="Имя", null=True, blank=True
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия", null=True, blank=True
    )
    phone_number = models.CharField(
        max_length=50, verbose_name="Номер телефона", null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    telegram_id = models.CharField(max_length=50, null=True, blank=True, verbose_name="Telegram")
    telegram_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="Telegram code")
    is_telegram_verified = models.BooleanField(default=False, verbose_name="Подтверждение Telegram ID")
    telegram_chat_id = models.CharField(null=True, blank=True, verbose_name="Telegram chat id")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]