from django.utils import timezone
from django.db import models
from users.models import User


class Habit(models.Model):
    """
    Модель привычки
    """
    title = models.CharField(max_length=100)  # название привычки
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # "хозяин" привычки
    place = models.CharField(max_length=100, blank=True, null=True)  # место выполнения
    time = models.TimeField(
        default=timezone.now
    )  # время, когда необходимо выполнять привычку
    action = models.CharField(
        max_length=100, blank=True, null=True
    )  # действие, которое надо выполнить
    is_healthy = models.BooleanField(default=True)  # флаг полезной привычки
    nice_habit = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )  # связанная приятная привычка
    period = models.IntegerField(default=7)  # периодичность выполнения
    last_action = models.DateTimeField(
        default=timezone.now
    )  # дата и время когда последний раз была выполнена привычка
    reward = models.CharField(
        max_length=100, blank=True, null=True
    )  # награда за выполнение полезной привычки
    action_time = models.IntegerField(default=120)  # время на выполнение действия
    is_public = models.BooleanField(default=False)  # флаг публичности

    def __str__(self):
        return f"{self.title} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["id", "title", "owner", "place"]
