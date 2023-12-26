from rest_framework import generics, status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from .authentication import Web3Authentication
from .models import EthAccount, Event
from .serializers import (EthAccountSerializer, EventSerializer,
                          Web3AuthSerializer)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class EthAccountNonceView(generics.RetrieveAPIView):
    serializer_class = EthAccountSerializer

    def get_object(self):
        address = self.kwargs.get('address')
        account, _ = EthAccount.objects.get_or_create(address=address)
        return account


class Web3AuthView(views.APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = Web3AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.validated_data['address']
        signature = serializer.validated_data['signature']

        account, created = EthAccount.objects.get_or_create(address=address)
        if created:
            # If the account is newly created, save to generate nonce
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
                # If authentication fails and account was newly created, delete it
                account.delete()
            return Response(
                {'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED
            )
