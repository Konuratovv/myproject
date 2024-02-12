from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.users.managers import CustomUserManager



# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(CustomUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    desription = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)