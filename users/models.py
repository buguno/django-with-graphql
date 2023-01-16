from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True, verbose_name="Email")

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
