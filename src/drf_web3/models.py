import hashlib
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


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
    message_to_sign = models.TextField(blank=True)

    def __str__(self):
        return self.username

    def generate_message_to_sign(self):
        timestamp = timezone.now()
        expiration_time = timestamp + timedelta(hours=1)
        unique_id = hashlib.sha256(
            f'{self.eth_address}{timestamp}{self.nonce}'.encode()
        ).hexdigest()
        self.message_to_sign = (
            f'Sign this message to authenticate. '
            f'Message ID: {unique_id}. '
            f'Timestamp: {timestamp.isoformat()}. '
            f'Valid until: {expiration_time.isoformat()}.'
        )
        self.nonce = uuid.uuid4()  # Update the nonce
        self.save()
