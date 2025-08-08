import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from django_plotly_dash import DjangoDash

from .models import Operation

# --- O Cérebro do Gráfico: A Lógica de Dados ---


def get_equity_curve_data(user_id):
    """
    Busca as operações fechadas de um usuário e calcula a curva de patrimônio.
    """
    # 1. Filtramos as operações: apenas as 'FECHADA' e do usuário específico.
    operations = Operation.objects.filter(
        user_id=user_id, status='FECHADA').order_by('end_date')

    if not operations.exists():
        # Se não houver operações, retornamos um DataFrame vazio para não dar erro.
        return pd.DataFrame(columns=['data', 'resultado_acumulado'])

    # 2. Criamos um DataFrame com o Pandas para facilitar os cálculos.
    data = list(operations.values('end_date', 'net_financial_result'))
    df = pd.DataFrame(data)

    # 3. Calculamos o resultado acumulado.
    df['resultado_acumulado'] = df['net_financial_result'].cumsum()
    df.rename(columns={'end_date': 'data'}, inplace=True)

    return df


# --- A Aparência do Gráfico: O Layout do Dash ---
app = DjangoDash('EquityCurve')

app.layout = html.Div([
    dcc.Graph(id='equity-curve-graph')
    # O gráfico será preenchido pela nossa função de callback,
    # que será chamada pelo template.
])

# Esta é a função que será chamada para atualizar o gráfico.
# Por enquanto, deixaremos ela "vazia". A mágica de conectar
# o usuário logado a ela acontecerá no template.


def serve_layout():
    # A lógica real será movida para o template para podermos passar o ID do usuário
    return html.Div()
