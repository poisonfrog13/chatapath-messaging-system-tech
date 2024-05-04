from django.db import models
from django.dispatch import receiver

from server.apps.authentication.models import ChatUser

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(
        ChatUser, on_delete=models.CASCADE, related_name="message_from"
    )
    recipient = models.ForeignKey(
        ChatUser, on_delete=models.CASCADE, related_name="message_to"
    )
    subject = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_unread = models.BooleanField(default=True)
