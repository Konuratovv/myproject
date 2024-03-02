from django.contrib import admin
from django.urls import include, path

from apps.webapp.views import post_detail_api_view, posts_api_view

urlpatterns = [
    path('posts/', posts_api_view),
    path('posts/<int:pk>/', post_detail_api_view),

]
