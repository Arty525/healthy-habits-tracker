from rest_framework.serializers import ValidationError
from tracker.models import Habit


class RewardValidator:
    """
    Проверяет наличие одновременно награды и приятной привычки при создании полезной привычки
    """

    def __init__(self, reward, nice_habit):
        self.reward = reward
        self.nice_habit = nice_habit

    def __call__(self, fields):
        if fields.get("reward") and fields.get("nice_habit"):
            raise ValidationError(
                "Нельзя одновременно добавить награду и приятную привычку."
            )


class ActionTimeValidator:
    """
    Проверяет, чтобы время выполнения привычки было не больше 120 секунд
    """

    def __init__(self, action_time):
        self.action_time = action_time

    def __call__(self, fields):
        action_time = fields.get("action_time")
        if action_time is not None:
            if not (0 < action_time < 120):
                raise ValidationError(
                    "Время выполнения привычки должно быть от 1 до 120 секунд."
                )


class NiceHabitValidator:
    """
    Проверяет, что поле nice_habit содержит только приятную привычку
    """

    def __init__(self, nice_habit):
        self.nice_habit = nice_habit

    def __call__(self, fields):
        if fields.get("nice_habit"):
            nice_habit = Habit.objects.get(pk=fields.get("nice_habit").pk)
            print(nice_habit.is_healthy)
            if nice_habit.is_healthy:
                raise ValidationError(
                    "Нельзя добавить полезную привычку в качестве связанной привычки."
                )


class NiceHabitRewardValidator:
    """
    Проверяет отсутствие награды и связанной привычки у приятной привычки
    """

    def __init__(self, nice_habit, reward, is_healthy):
        self.nice_habit = nice_habit
        self.reward = reward
        self.is_healthy = is_healthy

    def __call__(self, fields):
        if not fields.get("is_healthy"):
            if fields.get("nice_habit") or fields.get("reward"):
                raise ValidationError(
                    "Для приятной привычки нельзя добавить награду и связанную привычку"
                )


class PeriodValidator:
    """
    Проверяет, чтобы привычка выполнялась хотя бы 1 раз в неделю
    """

    def __init__(self, period):
        self.period = period

    def __call__(self, fields):
        period = fields.get("period")
        if period is not None:
            if not (0 < period <= 7):
                raise ValidationError("Период должен быть от 1 до 7 дней")
