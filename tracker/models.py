from datetime import timedelta

from django.db import models
from users.models import User


# Create your models here.
class NiceHabit(models.Model):
    '''
    Модель приятной привычки
    '''
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    is_healthy = models.BooleanField(default=False)
    period = models.CharField(max_length=10, blank=True, null=True, default='1 week')
    action_time = models.TimeField(default=timedelta(seconds=120))
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} - {self.owner} | healthy: {self.is_healthy}'


    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['title', 'owner', 'place']


class HealthyHabit(models.Model):
    '''
    Модель полезной привычки
    '''
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    is_healthy = models.BooleanField(default=True)
    nice_habit = models.ForeignKey(NiceHabit, on_delete=models.CASCADE, blank=True, null=True)
    period = models.CharField(max_length=10, blank=True, null=True, default='1 week')
    reward = models.CharField(max_length=100, blank=True, null=True)
    action_time = models.TimeField(default=timedelta(seconds=120))
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} - {self.owner} | healthy: {self.is_healthy}'


    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['title', 'owner', 'place']