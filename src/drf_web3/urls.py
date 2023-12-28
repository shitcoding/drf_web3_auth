from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, MessageView, Web3AuthView

router = DefaultRouter()
router.register('events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'message/<str:eth_address>/',
        MessageView.as_view(),
        name='message',
    ),
    path('auth/web3/', Web3AuthView.as_view(), name='web3-auth'),
]
