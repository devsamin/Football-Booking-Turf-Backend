from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'      # login হবে email দিয়ে
    REQUIRED_FIELDS = ['username', 'phone']  # superuser ও register সময় লাগবে

    def __str__(self):
        return self.email
