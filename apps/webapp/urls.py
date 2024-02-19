from django.contrib import admin
from django.urls import include, path

from apps.webapp.views import PostAPIView, PostDetailAPIView

urlpatterns = [
    path('posts/', PostAPIView.as_view()),
    path('detailed-post/<int:pk>/', PostDetailAPIView.as_view()),

]
