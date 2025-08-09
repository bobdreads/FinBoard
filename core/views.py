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
    """
    VERSÃO FINAL que exibe os dados reais do usuário.
    """
    operations = Operation.objects.filter(user=request.user)
    closed_operations = operations.filter(
        status='FECHADA', end_date__isnull=False)

    total_pl_converted = sum(convert_to_brl(op.net_financial_result, op.account.currency, op.end_date)
                             for op in closed_operations if op.net_financial_result is not None)

    trade_count = closed_operations.count()
    winning_trades = closed_operations.filter(
        net_financial_result__gt=0).count()
    win_rate = (winning_trades / trade_count * 100) if trade_count > 0 else 0

    # Lógica do Gráfico Real
    df = get_equity_curve_data(request.user.id)
    fig = go.Figure()
    if not df.empty:
        fig.add_trace(go.Scatter(x=df['data'], y=df['resultado_acumulado'],
                      mode='lines+markers', name='Patrimônio', line=dict(color='#6366F1', width=2)))

    fig.update_layout(
        title={'text': 'Curva de Patrimônio Acumulado (em BRL)', 'x': 0.5, 'font': {
            'color': 'white'}},
        xaxis_title={'text': 'Data', 'font': {'color': 'white'}},
        yaxis_title={'text': 'Resultado Acumulado (R$)', 'font': {
            'color': 'white'}},
        plot_bgcolor='rgba(17, 24, 39, 0)', paper_bgcolor='rgba(31, 41, 55, 0.8)', font_color="white",
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'), yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    app_context = {'EquityCurve': {'fig': fig}}

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
