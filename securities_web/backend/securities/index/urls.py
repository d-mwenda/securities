from django.urls import path

from .views import HomeView, RobotsView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("robots.txt", RobotsView.as_view(), name="robots")
]
