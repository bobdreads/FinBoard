import requests
from decimal import Decimal
from datetime import date, timedelta

# O cache continua sendo nosso aliado para performance
RATES_CACHE = {}


def get_exchange_rate(currency_code, date_obj):
    """
    Busca a taxa de câmbio (PTAX de venda) do Dólar para uma data específica,
    usando a API do Banco Central do Brasil.
    Se a data for um dia não-útil, busca o último dia útil anterior.
    """
    # Por enquanto, focamos na conversão USD -> BRL, que é a mais comum.
    if currency_code != 'USD':
        # Retorna 1 para não alterar moedas que não sejam dólar
        return Decimal('1.0')

    current_date = date_obj
    # Formato DD/MM/YYYY exigido pelo BCB
    date_str = current_date.strftime('%d/%m/%Y')

    # 1. Verifica o cache primeiro
    if date_str in RATES_CACHE:
        return RATES_CACHE[date_str]

    # 2. Loop para buscar a cotação, andando para trás nos dias se necessário
    for _ in range(10):  # Tentamos até 10 dias para trás para cobrir feriados longos
        try:
            formatted_date = current_date.strftime(
                '%m-%d-%Y')  # Formato MM-DD-YYYY para a URL
            # A URL busca a cotação PTAX para uma data específica
            url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{formatted_date}'&$top=100&$format=json"

            response = requests.get(url, timeout=10)  # Timeout de 10s
            response.raise_for_status()
            data = response.json()

            # Se a lista 'value' não estiver vazia, encontramos a cotação
            if data.get('value'):
                rate = data['value'][0].get('cotacaoVenda')
                if rate:
                    rate_decimal = Decimal(str(rate))
                    # Guarda a cotação no cache com a DATA ORIGINAL da consulta
                    RATES_CACHE[date_str] = rate_decimal
                    return rate_decimal

            # Se não encontrou, tenta o dia anterior
            current_date -= timedelta(days=1)

        except requests.exceptions.RequestException as e:
            print(f"ERRO: Falha ao acessar a API do BCB: {e}")
            return None  # Retorna None em caso de falha de conexão

    print(
        f"AVISO: Não foi possível encontrar a cotação para {currency_code} na data {date_str} ou nos 10 dias anteriores.")
    return None


def convert_to_brl(amount, currency_code, date_obj):
    """
    Converte um valor de uma moeda estrangeira para BRL.
    """
    if currency_code == 'BRL' or amount is None:
        return amount

    # Passamos apenas a data
    rate = get_exchange_rate(currency_code, date_obj.date())

    if rate:
        converted_amount = Decimal(str(amount)) * rate
        return converted_amount.quantize(Decimal('0.01'))

    # Se não conseguiu nenhuma cotação, retorna o valor original para não quebrar os cálculos
    return amount
