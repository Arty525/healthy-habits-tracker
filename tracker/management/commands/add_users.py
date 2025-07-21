import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from users.models import User


class Command(BaseCommand):
    help = "Creates new test users"

    def handle(self, *args, **options):
        User.objects.all().delete()

        # Добавляем тестовых пользователей с паролем password123
        call_command("loaddata", os.path.join("fixtures", "users_fixture.json"))

        self.stdout.write(self.style.SUCCESS("Successfully created new users"))
