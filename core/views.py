# Substitua o conteúdo de: bobdreads/finboard/FinBoard-4aa8007547cbb92200d5fbe4c83e75b99a1e9624/core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from dashboard.models import Operation
from .forms import SignUpForm
import plotly.graph_objects as go

# --- IMPORTAÇÕES CORRIGIDAS ---
from dashboard.currency_converter import convert_to_brl
from dashboard.dash_apps import get_equity_curve_data


@login_required
def home(request):
    # A lógica para buscar seus KPIs permanece a mesma
    operations = Operation.objects.filter(user=request.user)
    closed_operations = operations.filter(
        status='FECHADA', end_date__isnull=False)
    total_pl_converted = sum(convert_to_brl(op.net_financial_result, op.account.currency, op.end_date)
                             for op in closed_operations if op.net_financial_result is not None)
    trade_count = closed_operations.count()
    winning_trades = closed_operations.filter(
        net_financial_result__gt=0).count()
    win_rate = (winning_trades / trade_count * 100) if trade_count > 0 else 0

    # --- LÓGICA DO GRÁFICO ATUALIZADA COM ESTILO E VERIFICAÇÃO DE DADOS ---
    df = get_equity_curve_data(request.user.id)
    fig = go.Figure()

    title_text = 'Curva de Patrimônio Acumulado (em BRL)'
    # Se não houver dados, alteramos o título para informar o usuário
    if df.empty:
        title_text = 'Curva de Patrimônio (Sem operações fechadas para exibir)'

    fig.add_trace(go.Scatter(
        x=df['data'],
        y=df['resultado_acumulado'],
        mode='lines+markers',
        name='Patrimônio',
        line=dict(color='#6366F1', width=2)  # Cor da linha (indigo)
    ))

    fig.update_layout(
        title={'text': title_text, 'x': 0.5, 'font': {'color': 'white'}},
        # CORREÇÃO: Fundo transparente para se mesclar ao site
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="white",  # Cor da fonte para os eixos e legendas
        # CORREÇÃO: Responsividade
        autosize=True,
        # Cor das linhas de grade
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        margin=dict(l=50, r=20, t=60, b=40)  # Ajuste de margens
    )

    app_context = {'EquityCurve': {'fig': fig}}
    # --- FIM DA ATUALIZAÇÃO ---

    context = {
        'operations': operations.order_by('-start_date'),
        'dash_context': app_context,
        'total_pl': total_pl_converted,
        'trade_count': trade_count,
        'win_rate': win_rate,
    }
    return render(request, 'core/home.html', context)


def register(request):
    """
    Processa o formulário de cadastro de novos usuários.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'core/register.html', {'form': form})
