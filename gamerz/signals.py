from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *



@receiver(post_save, sender=OngoingGame)
def log_user_login(sender, request, user, **kwargs):
    LoginLog.objects.create(user=user)
