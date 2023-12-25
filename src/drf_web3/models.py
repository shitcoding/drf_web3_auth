from django.db import models


class Event(models.Model):
    tx_hash = models.CharField(max_length=66)
    from_address = models.CharField(max_length=42)
    to_address = models.CharField(max_length=42)
    value = models.BigIntegerField()
    created_at = models.DateTimeField()

    def __str__(self):
        return self.tx_hash