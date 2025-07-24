from rest_framework import serializers
from tracker.models import Habit
from tracker.validators import (NiceHabitRewardValidator, ActionTimeValidator,
                                PeriodValidator, RewardValidator, NiceHabitValidator)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [ActionTimeValidator(action_time="action_time"), PeriodValidator(period="period"),
                      NiceHabitRewardValidator(reward="reward", nice_habit="nice_habit", is_healthy="is_healthy"),
                      RewardValidator(reward="reward", nice_habit="nice_habit"),
                      NiceHabitValidator(nice_habit="nice_habit")]
