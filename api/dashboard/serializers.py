# api/dashboard/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Trade, Portfolio, Strategy


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

# NOVO SERIALIZER PARA O MODELO TRADE


class TradeSerializer(serializers.ModelSerializer):
    # Usamos source para aceder a campos de modelos relacionados
    portfolio_name = serializers.CharField(
        source='portfolio.name', read_only=True)
    user_username = serializers.CharField(
        source='user.username', read_only=True)

    class Meta:
        model = Trade
        # Lista de campos do novo modelo que queremos expor na API
        fields = [
            'id',
            'symbol',
            'side',
            'fees',
            'net_result',
            'is_open',
            'created_at',
            'portfolio',  # ID do portfólio
            'portfolio_name',
            'user',  # ID do utilizador
            'user_username',
        ]
