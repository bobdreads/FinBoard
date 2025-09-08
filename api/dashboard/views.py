# api/dashboard/views.py

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

# 1. Importamos os nossos NOVOS modelos e serializers
from .models import Trade
from .serializers import UserSerializer, TradeSerializer

# --- Views da API ---


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

# NOVA VIEW DA API PARA LISTAR TRADES


class TradeListAPIView(generics.ListAPIView):
    """
    Esta view da API lista todos os trades do utilizador autenticado.
    """
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]  # Mantemos a segurança

    def get_queryset(self):
        # A query agora busca por Trades, não por Operations
        return Trade.objects.filter(user=self.request.user).order_by('-created_at')
