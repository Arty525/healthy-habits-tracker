from celery import shared_task
from django.utils import timezone
from datetime import timedelta, time, datetime
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
    now_datetime = datetime.combine(datetime.today(), now_time)
    time_plus_1h = (now_datetime + timedelta(hours=1)).time()
    time_plus_10min = (now_datetime + timedelta(minutes=10)).time()
    habits = Habit.objects.all()
    for habit in habits:
        if (timezone.localtime(timezone.now()) - timedelta(days=habit.period)).date() == habit.last_action.date():
            if time_plus_1h == habit.time:
                print(f'через 1 час у вас запланировано {habit}')
            if time_plus_10min == habit.time:
                print(f'через 10 минут у вас запланировано {habit}')

# Надо добавить проверку периодичности выполнения и сделать проверку на время выполнения.