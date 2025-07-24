import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from tracker.models import Habit


class Command(BaseCommand):
    help = "Creates new test habits"

    def handle(self, *args, **options):
        Habit.objects.all().delete()

        # Добавляем тестовые приятные привычки
        call_command("loaddata", os.path.join("fixtures", "habits_fixture.json"))

        self.stdout.write(self.style.SUCCESS("Successfully created new habits"))
