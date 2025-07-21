import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from tracker.models import HealthyHabit, NiceHabit
from users.models import User


class Command(BaseCommand):
    help = "Creates new records in all tables of the database"

    def handle(self, *args, **options):
        HealthyHabit.objects.all().delete()
        NiceHabit.objects.all().delete()
        User.objects.all().delete()

        # Добавляем тестовых пользователей с паролем password123
        call_command("loaddata", os.path.join("fixtures", "users_fixture.json"))

        # Добавляем тестовые приятные привычки
        call_command("loaddata", os.path.join("fixtures", "nice_habits_fixture.json"))

        # Добавляем тестовые полезные привычки
        call_command("loaddata", os.path.join("fixtures", "healthy_habits_fixture.json"))

        self.stdout.write(self.style.SUCCESS("Successfully created all tables"))
