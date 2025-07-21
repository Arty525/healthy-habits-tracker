import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from tracker.models import NiceHabit


class Command(BaseCommand):
    help = "Creates new test nice habits"

    def handle(self, *args, **options):
        NiceHabit.objects.all().delete()

        # Добавляем тестовые приятные привычки
        call_command("loaddata", os.path.join("fixtures", "nice_habits_fixture.json"))

        self.stdout.write(self.style.SUCCESS("Successfully created new nice habits"))
