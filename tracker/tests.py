from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from tracker.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        # создаем тестового пользователя
        self.user = User.objects.create_user(
            email="test@test.ru", password="testpass123"
        )

        # создаем второго тестового пользователя
        self.second_user = User.objects.create_user(
            email="test2@testmail.ru", password="testpass123"
        )

        # создаем тестовую приятную привычку
        self.nice_habit = Habit.objects.create(
            title="Утренний кофе",
            owner=self.user,
            place="Кухня",
            time="08:45:00",
            action="Выпить чашку кофе",
            is_healthy=False,
            nice_habit=None,
            period=1,
            last_action="2025-07-25T08:45:00+03:00",
            reward=None,
            action_time=120,
            is_public=True,
        )

        # создаем тестовую полезную привычку
        self.healthy_habit = Habit.objects.create(
            title="Контрастный душ",
            owner=self.user,
            place="Ванная",
            time="08:15:00",
            action="Принять душ",
            is_healthy=True,
            nice_habit=self.nice_habit,
            period=1,
            last_action="2025-07-25T08:15:00+03:00",
            reward=None,
            action_time=120,
            is_public=True,
        )

        # создаем тестовую полезную привычку для второго пользователя
        self.second_healthy_habit = Habit.objects.create(
            title="Подтягивания",
            owner=self.second_user,
            place="Турник",
            time="18:15:00",
            action="Подтянуться 10 раз",
            is_healthy=True,
            period=2,
            last_action="2025-07-24T18:15:00+03:00",
            reward="Выпить йогурт",
            action_time=100,
            is_public=True,
        )

        self.client = APIClient()

    def test_create_habit(self):
        """Тестирование создания привычки"""
        url = reverse("tracker:tracker-list")
        data = {
            "title": "Прогулка после еды",
            "place": "Улица",
            "time": "21:30:00",
            "action": "Гулять",
            "is_healthy": True,
            "period": 1,
            "last_action": "2025-07-25T21:30:00+03:00",
            "reward": "Шоколадка",
            "action_time": 110,
            "is_public": True,
        }
        self.client.force_authenticate(user=self.second_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Прогулка после еды")
        self.assertEqual(Habit.objects.all().count(), 4)
        Habit.objects.get(pk=response.data["id"]).delete()

    def test_create_habit_unauthorized(self):
        """Тестирование создания привычки без авторизации"""
        url = reverse("tracker:tracker-list")
        data = {
            "title": "Прогулка после еды",
            "place": "Улица",
            "time": "21:30:00",
            "action": "Гулять",
            "is_healthy": True,
            "period": 1,
            "last_action": "2025-07-25T21:30:00+03:00",
            "reward": "Шоколадка",
            "action_time": 110,
            "is_public": True,
        }
        response = self.client.get(url)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_habits(self):
        """Тестирование получения списка привычек"""

        # для первого пользователя
        url = reverse("tracker:tracker-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

        # для второго пользователя
        self.client.force_authenticate(user=self.second_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_list_habits_unauthorized(self):
        """Тестирование получения списка привычек без авторизации"""

        url = reverse("tracker:tracker-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_habit(self):
        """Тестирование получения одной привычки"""
        url = reverse("tracker:tracker-detail", kwargs={"pk": self.healthy_habit.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Контрастный душ")

        self.client.force_authenticate(user=self.second_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_habit(self):
        """Тестирование обновления привычки"""
        url = reverse(
            "tracker:tracker-detail", kwargs={"pk": self.second_healthy_habit.pk}
        )
        self.client.force_authenticate(user=self.second_user)
        data = {"title": "Подтягивания (upd)"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Подтягивания (upd)")

        self.client.force_authenticate(user=self.user)
        data = {"title": "Подтягивания"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_habit(self):
        """Тестирование удаления привычки"""
        test_habit = Habit.objects.create(
            title="Test Habit",
            place="Test Place",
            time="21:30:00",
            action="Test Action",
            is_healthy=True,
            period=1,
            last_action="2025-07-25T21:30:00+03:00",
            reward="Test Reward",
            action_time=110,
            is_public=False,
            owner=self.user,
        )
        url = reverse("tracker:tracker-detail", kwargs={"pk": test_habit.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Habit")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_public_habits_list(self):
        """Тестирование получения списка публичных привычек"""
        url = reverse("tracker:public_habits")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)

    def test_user_habits_list(self):
        """Тестирование получения списка привычек текущего пользователя"""
        pass

    def test_habit_action_time_validation(self):
        """Тестирование валидации времени выполнения привычки"""
        url = reverse("tracker:tracker-list")
        data = {
            "title": "Test",
            "place": "Test",
            "time": "21:30:00",
            "action": "Test",
            "is_healthy": True,
            "period": 1,
            "last_action": "2025-07-25T21:30:00+03:00",
            "reward": "Test",
            "action_time": 130,
            "is_public": True,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_period_validation(self):
        """Тестирование валидации привычки"""
        url = reverse("tracker:tracker-list")
        data = {
            "title": "Test",
            "place": "Test",
            "time": "21:30:00",
            "action": "Test",
            "is_healthy": True,
            "period": 10,
            "last_action": "2025-07-25T21:30:00+03:00",
            "reward": "Test",
            "action_time": 110,
            "is_public": True,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CustomCommandsTestCase(TestCase):
    def test_add_users(self):
        """Тестирование команды добавления пользователей"""
        call_command("add_users")
        self.assertEqual(User.objects.all().count(), 10)

    def test_add_habits(self):
        """Тестирование команды добавления привычек"""
        if User.objects.all().count() == 0:
            call_command("add_users")
        call_command("add_habits")
        self.assertEqual(Habit.objects.all().count(), 30)

    def test_add_all_data(self):
        """Тестирование команды добавления данных"""
        call_command("add_all_data")
        self.assertEqual(User.objects.all().count(), 10)
        self.assertEqual(Habit.objects.all().count(), 30)
