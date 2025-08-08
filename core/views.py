from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from dashboard.models import Operation
from .forms import SignUpForm
from dashboard.dash_apps import get_equity_curve_data
import plotly.graph_objects as go

# Create your views here.


@login_required
def home(request):
    """
    Esta view renderiza a página inicial do projeto.
    """
    # --- 1. Buscando Dados ---
    operations = Operation.objects.filter(user=request.user)
    closed_operations = operations.filter(status='FECHADA')

    # --- 2. Calculando KPIs ---
    total_pl = closed_operations.aggregate(Sum('net_financial_result'))[
        'net_financial_result__sum'] or 0
    trade_count = closed_operations.count()

    winning_trades = closed_operations.filter(
        net_financial_result__gt=0).count()
    win_rate = (winning_trades / trade_count * 100) if trade_count > 0 else 0

    # --- 3. Preparando Gráfico (Lógica que já tínhamos) ---
    df = get_equity_curve_data(request.user.id)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['data'], y=df['resultado_acumulado'], mode='lines+markers',
                             name='Patrimônio', line=dict(color='#6366F1', width=2)))
    fig.update_layout(
        title={'text': 'Curva de Patrimônio Acumulado',
               'x': 0.5, 'font': {'color': 'white'}},
        xaxis_title={'text': 'Data', 'font': {'color': 'white'}},
        yaxis_title={'text': 'Resultado Acumulado',
                     'font': {'color': 'white'}},
        plot_bgcolor='rgba(17, 24, 39, 0)',
        paper_bgcolor='rgba(31, 41, 55, 0.8)',
        font_color="white",
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    # --- 4. Montando o Contexto para o Template ---
    app_context = {'EquityCurve': {'fig': fig}}

    context = {
        'operations': operations,
        'dash_context': app_context,
        # Enviando os novos KPIs para o template
        'total_pl': total_pl,
        'trade_count': trade_count,
        'win_rate': win_rate,
    }

    return render(request, 'core/home.html', context)


def register(request):
    """
    Processa o formulário de cadastro de novos usuários.
    """
    if request.method == 'POST':
        # Se o formulário foi enviado (método POST), crie uma instância dele
        # com os dados que o usuário enviou.
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Se o formulário for válido, salve o novo usuário no banco de dados.
            user = form.save()
            # Faça o login automático do usuário recém-criado.
            login(request, user)
            # Redirecione o usuário para a página inicial.
            return redirect('core:home')
    else:
        # Se for a primeira vez que o usuário visita a página (método GET),
        # apenas crie uma instância de um formulário em branco.
        form = SignUpForm()

    # Renderize o template, passando o formulário como contexto.
    return render(request, 'core/register.html', {'form': form})
