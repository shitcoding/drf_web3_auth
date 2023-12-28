from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser
from .utils import verify_signature


class Web3Authentication(BaseAuthentication):
    def authenticate(self, request):
        """Override standard auth method."""
        return None

    def authenticate_signature(self, eth_address, message, signature):
        if not verify_signature(eth_address, message, signature):
            raise AuthenticationFailed('Invalid or expired signature')

        user, created = CustomUser.objects.get_or_create(
            eth_address=eth_address
        )
        if created:
            user.username = eth_address
            user.set_unusable_password()
            user.save()

        return user
