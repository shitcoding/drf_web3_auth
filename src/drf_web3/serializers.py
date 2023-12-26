from rest_framework import serializers

from .models import EthAccount, Event


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


class EthAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EthAccount
        fields = ['address', 'nonce']


class Web3AuthSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=42)
    signature = serializers.CharField(max_length=255)
