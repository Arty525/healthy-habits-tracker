from celery import shared_task
from django.utils import timezone
from datetime import timedelta, time
from .models import User, Habit
from .services import send_telegram_message


@shared_task
def habits_reminder():
    '''
    Проходит по всем привычкам, если у пользователя есть телеграм и до выполнения привычки остался один час
    или привычка должна быть выполнена в течение 10 минут, отправляет уведомление через телеграм.
    '''
    now_hours = timezone.localtime(timezone.now()).hour
    print(f'now hour: {now_hours}')
    now_minutes = timezone.localtime(timezone.now()).minute
    print(f'now minute: {now_minutes}')
    now_time = time(hour=now_hours, minute=now_minutes)

    habits = Habit.objects.filter(time=now_time + timedelta(seconds=600).seconds)
    for habit in habits:
        send_telegram_message(f'Через 10 минут необходимо {habit}')

    habits = Habit.objects.filter(time=now_time + timedelta(hours=1).seconds)
    for habit in habits:
        send_telegram_message(f'Через 1 час необходимо {habit}')