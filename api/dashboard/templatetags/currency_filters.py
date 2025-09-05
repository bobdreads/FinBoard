from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from decimal import Decimal

register = template.Library()


@register.filter(name='format_currency')
def format_currency(value, currency_code):
    """
    Formata um valor numérico como moeda, com base no código da moeda.
    Exemplo de uso: {{ account.current_balance|format_currency:account.currency }}
    """
    try:
        # Garante que o valor seja um Decimal
        value = Decimal(value)
    except (ValueError, TypeError):
        return value

    # Formata o número com separador de milhar
    # Usamos um truque para trocar a vírgula do padrão americano por um ponto temporário
    formatted_value = intcomma(value).replace(
        ",", "TEMP_COMMA").replace(".", ",").replace("TEMP_COMMA", ".")

    if currency_code == 'BRL':
        return f"R$ {formatted_value}"
    elif currency_code == 'USD':
        return f"US$ {formatted_value}"
    else:
        # Caso padrão para outras moedas
        return f"{currency_code} {formatted_value}"
