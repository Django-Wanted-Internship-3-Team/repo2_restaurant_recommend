from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from restaurants_recommendation.users.managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    latitude = models.CharField(max_length=32)
    longitude = models.CharField(max_length=32)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_lunch_recommendation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: models.Manager = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
