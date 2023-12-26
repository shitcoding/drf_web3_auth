from django.contrib.admin.filters import ValidationError
from django.contrib.auth.models import User
from rest_framework import generics, status, views, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .authentication import Web3Authentication
from .models import CustomUser, Event
from .serializers import (EthAccountNonceSerializer, EventSerializer,
                          Web3AuthSerializer)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class EthAccountNonceView(generics.RetrieveAPIView):
    serializer_class = EthAccountNonceSerializer

    def get_object(self):
        eth_address = self.kwargs.get('eth_address')
        if not eth_address:
            # Handle the case where eth_address is not provided
            raise ValidationError('Ethereum address is required.')

        account, created = CustomUser.objects.get_or_create(
            username=eth_address, eth_address=eth_address
        )
        if created:
            # Set an unusable password as this user will use Web3 Auth
            account.set_unusable_password()
            account.save()
        return account


class Web3AuthView(views.APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = Web3AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        eth_address = serializer.validated_data['eth_address']
        signature = serializer.validated_data['signature']

        account, created = CustomUser.objects.get_or_create(
            username=eth_address, eth_address=eth_address
        )
        if created:
            # Set an unusable password as this user will use Web3 Auth
            account.set_unusable_password()
            account.save()

        try:
            Web3Authentication().authenticate_signature(account, signature)
            refresh = RefreshToken.for_user(account)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            )
        except AuthenticationFailed as e:
            if created:
                account.delete()  # Delete the account if it was newly created and authentication failed
            return Response(
                {'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED
            )
