from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Event

eth_address_validator = RegexValidator(regex='^0x[a-fA-F0-9]{40}$')


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


class MessageSerializer(serializers.Serializer):
    eth_address = serializers.CharField(
        max_length=42, validators=[eth_address_validator]
    )
    message = serializers.CharField()


class Web3AuthSerializer(serializers.Serializer):
    eth_address = serializers.CharField(
        max_length=42, validators=[eth_address_validator]
    )
    message = serializers.CharField()
    signature = serializers.CharField(max_length=132)

    def validate(self, data):
        if (
            not data.get('eth_address')
            or not data.get('message')
            or not data.get('signature')
        ):
            raise ValidationError(
                'Ethereum address, message and signature are required.'
            )
        return data
