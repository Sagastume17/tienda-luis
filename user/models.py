from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    rol = models.CharField(max_length=250, null=True, blank=True)
    tienda = models.CharField(max_length=550, null=True, blank=True)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.username
