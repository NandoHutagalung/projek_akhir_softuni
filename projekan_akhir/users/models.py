from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('member', 'Member'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='viewer')

    def __str__(self):
        return f"{self.username} - {self.get_full_name()} ({self.role})"
