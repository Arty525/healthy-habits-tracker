from django.urls import path, include
from rest_framework import routers
from tracker import views
from tracker.views import PublicHabitsAPIView, TestTGAPIView

app_name = "tracker"
router = routers.DefaultRouter()
router.register(r'tracker', views.HabitsViewSet, basename='tracker')
urlpatterns = [
    path('tracker/public/', PublicHabitsAPIView.as_view(), name='public_habits'),
    path('tracker/tg/', TestTGAPIView.as_view(), name='tg'),
] + router.urls
