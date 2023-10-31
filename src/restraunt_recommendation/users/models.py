# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('계정명은 반드시 필요합니다!')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        return self.create_user(username, password, **extra_fields)
    

class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    latitude = models.CharField(max_length=32, null=True)
    longitude = models.CharField(max_length=32, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_lunch_recommend = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS =[]


    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin