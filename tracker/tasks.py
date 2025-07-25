from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User


@shared_task
def habits_reminder():
    Habit.objects.filter(
        last_login__lt=(timezone.now() - timedelta(days=30)), is_active=True
    ).update(is_active=False)
    return "Пользователи заблокированы"
