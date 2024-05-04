from django.db import models

from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class ChatUser(AbstractUser):
    phone_number = PhoneNumberField(null=False, blank=False)
