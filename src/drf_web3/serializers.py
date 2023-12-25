from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'tx_hash',
            'from_address',
            'to_address',
            'value',
            'created_at',
        ]
