import uuid

from eth_account import Account
from eth_account.messages import encode_defunct
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import EthAccount


class Web3Authentication(BaseAuthentication):
    def authenticate(self, request):
        address = request.data.get('address')
        signature = request.data.get('signature')

        if not address or not signature:
            return None

        try:
            account = EthAccount.objects.get(address=address)
        except EthAccount.DoesNotExist:
            raise AuthenticationFailed('No such user')

        message = f'I am signing my one-time nonce: {account.nonce}'
        message_encoded = encode_defunct(text=message)
        signer_address = Account.recover_message(
            message_encoded, signature=signature
        )

        if signer_address.lower() == address.lower():
            account.nonce = (
                uuid.uuid4()
            )  # Update nonce after successful authentication
            account.save()
            return (account, None)

        raise AuthenticationFailed('Invalid signature')

    def authenticate_signature(self, account, signature):
        message = f'I am signing my one-time nonce: {account.nonce}'
        print(message)
        message_encoded = encode_defunct(text=message)
        signer_address = Account.recover_message(
            message_encoded, signature=signature
        )

        if signer_address.lower() != account.address.lower():
            raise AuthenticationFailed('Invalid signature')

        # Update nonce after successful authentication
        account.nonce = uuid.uuid4()
        account.save()
