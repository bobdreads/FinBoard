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
    portfolio_name = serializers.CharField(
        source='portfolio.name', read_only=True)
    user_username = serializers.CharField(
        source='user.username', read_only=True)
    # Adicionamos um campo para a versão "legível" do status
    status_display = serializers.CharField(
        source='get_status_display', read_only=True)

    class Meta:
        model = Trade
        fields = [
            'id',
            'symbol',
            'side',
            'fees',
            'net_result',
            'status',  # <-- O campo 'status' (ex: "OPEN")
            'status_display',  # <-- A versão legível (ex: "Em Aberto")
            'created_at',
            'portfolio',
            'portfolio_name',
            'user',
            'user_username',
        ]
