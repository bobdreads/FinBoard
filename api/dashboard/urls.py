# api/dashboard/urls.py

from django.urls import path
from .views import TradeListAPIView  # Importamos a nossa nova e única view

app_name = 'dashboard'

urlpatterns = [
    # O único endpoint que o dashboard serve agora é a lista de trades
    path('api/trades/', TradeListAPIView.as_view(), name='api_trade_list'),
]
