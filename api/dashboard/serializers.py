from rest_framework import serializers
from .models import Operation


class OperationSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Operation.
    Converte os dados do modelo para o formato JSON e vice-versa.
    """
    strategy_name = serializers.CharField(
        source='strategy.name', read_only=True)
    account_name = serializers.CharField(source='account.name', read_only=True)
    asset_ticker = serializers.CharField(source='asset.ticker', read_only=True)

    # O método 'get_total_price' no seu modelo não existe, vamos calcular o resultado financeiro
    # Se você tiver um campo de resultado no modelo, podemos usá-lo. Por agora, vamos usar 'net_financial_result'
    financial_result = serializers.DecimalField(
        source='net_financial_result', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Operation
        # Incluímos todos os campos do modelo e os campos extras que criamos
        fields = [
            'id',
            'user',
            'account_name',
            'strategy_name',
            'asset_ticker',
            'status',
            'start_date',
            'end_date',
            'financial_result',
        ]
