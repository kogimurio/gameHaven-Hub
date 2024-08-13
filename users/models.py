from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICE = (
        ('GAMER', 'GAMER'),
        ('EMPLOYEE', 'EMPLOYEE'),
        ('ADMIN', 'ADMIN'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default='GAMER')

    
