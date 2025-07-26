from django.urls import path
from rest_framework import routers
from tracker import views
from tracker.views import PublicHabitsAPIView


app_name = "tracker"
router = routers.DefaultRouter()
router.register(r"tracker", views.HabitsViewSet, basename="tracker")
urlpatterns = [
    path("tracker/public/", PublicHabitsAPIView.as_view(), name="public_habits"),
] + router.urls
