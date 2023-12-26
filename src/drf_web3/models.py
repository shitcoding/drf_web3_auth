import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Event(models.Model):
    tx_hash = models.CharField(max_length=66, unique=True)
    from_address = models.CharField(max_length=42)
    to_address = models.CharField(max_length=42)
    value = models.BigIntegerField()
    created_at = models.DateTimeField()

    def __str__(self):
        return self.tx_hash


class CustomUser(AbstractUser):
    eth_address = models.CharField(max_length=42, unique=True)
    nonce = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username
