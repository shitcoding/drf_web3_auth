from rest_framework import generics, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .authentication import Web3Authentication
from .models import Event
from .serializers import EventSerializer, MessageSerializer, Web3AuthSerializer
from .utils import generate_message


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class MessageView(generics.RetrieveAPIView):
    serializer_class = MessageSerializer

    def get(self, request, eth_address):
        message_data = generate_message(eth_address)
        return Response(message_data)


class Web3AuthView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = Web3AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = Web3Authentication().authenticate_signature(
            serializer.validated_data['eth_address'],
            serializer.validated_data['message'],
            serializer.validated_data['signature'],
        )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        )
