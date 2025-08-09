import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from django_plotly_dash import DjangoDash

from .models import Operation
from .currency_converter import convert_to_brl

# --- O Cérebro do Gráfico: A Lógica de Dados ---


def get_equity_curve_data(user_id):
    """
    Busca as operações fechadas de um usuário e calcula a curva de patrimônio,
    convertendo todos os resultados para BRL.
    """
    operations = Operation.objects.filter(
        user_id=user_id, status='FECHADA', end_date__isnull=False
    ).order_by('end_date')

    if not operations.exists():
        return pd.DataFrame(columns=['data', 'resultado_acumulado'])

    converted_data = []
    for op in operations:
        converted_result = convert_to_brl(
            op.net_financial_result,
            op.account.currency,
            op.end_date
        )
        converted_data.append({
            'end_date': op.end_date,
            'converted_result': converted_result
        })

    df = pd.DataFrame(converted_data)
    df['resultado_acumulado'] = df['converted_result'].cumsum()
    df.rename(columns={'end_date': 'data'}, inplace=True)

    return df


# --- A Aparência do Gráfico: O Layout do Dash (sem alterações) ---
app = DjangoDash('EquityCurve')

app.layout = html.Div([
    dcc.Graph(id='equity-curve-graph')
])


def serve_layout():
    return html.Div()
