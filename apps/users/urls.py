from django.contrib import admin
from django.urls import include, path

from apps.users.views import LoginAPIView, RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view())
]
