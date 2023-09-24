from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from users_app.managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    username = None
    email = models.EmailField("email address", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
