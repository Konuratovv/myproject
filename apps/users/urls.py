from django.contrib import admin
from django.urls import include, path

from apps.users.views import LoginAPIView, ProfileAPIView, RegisterAPIView, UpdateProfileAPIView, EmailVerificationAPIView, FollowUserAPIView, UnfollowUserAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('update-profile/', UpdateProfileAPIView.as_view()),
    path('verify-email/', EmailVerificationAPIView.as_view()),
    path('follow-user/', FollowUserAPIView.as_view()),
    path('unfollow-user/', UnfollowUserAPIView.as_view()),
]
