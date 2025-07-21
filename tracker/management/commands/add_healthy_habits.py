import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from tracker.models import HealthyHabit


class Command(BaseCommand):
    help = "Creates new test healthy habits"

    def handle(self, *args, **options):
        HealthyHabit.objects.all().delete()

        # Добавляем тестовые полезные привычки
        call_command("loaddata", os.path.join("fixtures", "healthy_habits_fixture.json"))

        self.stdout.write(self.style.SUCCESS("Successfully created new healthy habits"))
