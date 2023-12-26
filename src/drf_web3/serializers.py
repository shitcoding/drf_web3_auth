from rest_framework import serializers

from .models import CustomUser, Event


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


class EthAccountMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['eth_address', 'message_to_sign']


class Web3AuthSerializer(serializers.Serializer):
    eth_address = serializers.CharField(max_length=42)
    signature = serializers.CharField(max_length=255)
