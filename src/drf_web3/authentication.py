import uuid

from django.utils import timezone
from datetime import UTC
from eth_account import Account
from eth_account.messages import encode_defunct
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser


class Web3Authentication(BaseAuthentication):
    def authenticate(self, request):
        eth_address = request.data.get('eth_address')
        signature = request.data.get('signature')

        if not eth_address or not signature:
            return None

        try:
            account = CustomUser.objects.get(eth_address=eth_address)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Account does not exist')

        message = f'I am signing my one-time nonce: {account.nonce}'
        message_encoded = encode_defunct(text=message)
        signer_address = Account.recover_message(
            message_encoded, signature=signature
        )

        if signer_address.lower() == eth_address.lower():
            account.nonce = uuid.uuid4()
            account.save()
            return (account, None)

        raise AuthenticationFailed('Invalid signature')

    def authenticate_signature(self, account, signature):
        message = account.message_to_sign
        message_encoded = encode_defunct(text=message)
        signer_address = Account.recover_message(
            message_encoded, signature=signature
        )

        # Parse message expiration time and make it timezone aware
        expiration_str = message.split('Valid until: ')[1].split('.')[0]
        expiration_time = timezone.datetime.fromisoformat(expiration_str)
        expiration_time = timezone.make_aware(expiration_time, UTC)

        if timezone.now() > expiration_time:
            raise AuthenticationFailed('Message expired')

        if signer_address.lower() != account.eth_address.lower():
            raise AuthenticationFailed('Invalid signature')

        account.generate_message_to_sign()
