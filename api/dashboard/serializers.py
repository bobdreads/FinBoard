from rest_framework import serializers
from .models import Operation


class OperationSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Operation.
    Converte os dados do modelo para o formato JSON e vice-versa.
    """
    # Adiciona o nome da estratégia para facilitar a exibição no frontend
    strategy_name = serializers.CharField(
        source='strategy.name', read_only=True)
    # Adiciona o nome da conta para facilitar
    account_name = serializers.CharField(source='account.name', read_only=True)

    class Meta:
        model = Operation
        # Incluímos todos os campos do modelo e os campos extras que criamos
        fields = [
            'id',
            'strategy',
            'strategy_name',
            'account',
            'account_name',
            'date',
            'type',
            'asset',
            'quantity',
            'price',
            'get_total_price',  # Usando o método do modelo
            'result',
            'created_at'
        ]
