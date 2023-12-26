from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EthAccountNonceView, EventViewSet, Web3AuthView

router = DefaultRouter()
router.register('events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    path('nonce/<str:address>/', EthAccountNonceView.as_view(), name='nonce'),
    path('auth/web3/', Web3AuthView.as_view(), name='web3-auth'),
]
