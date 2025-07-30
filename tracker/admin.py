from django.contrib import admin
from django.utils.formats import date_format
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "owner",
        "place",
        "action",
        "is_healthy",
        "nice_habit",
        "period",
        "reward",
        "action_time",
        "is_public",
        "time",
    )
    list_display = (
        "id",
        "title",
        "owner",
        "place",
        "is_healthy",
        "is_public",
        "formatted_time",
        "period",
    )
    list_filter = ("is_healthy", "is_public")
    search_fields = ("title", "owner", "place", "time", "period")

    def formatted_time(self, obj):
        return date_format(obj.time, "H:i")  # 24-часовой формат без секунд

    formatted_time.short_description = "Время"  # Заголовок колонки
    formatted_time.admin_order_field = "time"  # Сортировка по исходному полю
