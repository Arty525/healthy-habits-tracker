import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from tracker.models import Habit
from users.models import User


class Command(BaseCommand):
    help = "Creates new records in all tables of the database"

    def handle(self, *args, **options):
        Habit.objects.all().delete()
        User.objects.all().delete()

        # Добавляем тестовых пользователей с паролем password123
        call_command("loaddata", os.path.join("fixtures", "users_fixture.json"))

        # Добавляем тестовые привычки
        call_command("loaddata", os.path.join("fixtures", "habits_fixture.json"))

        self.stdout.write(self.style.SUCCESS("Successfully created all tables"))
