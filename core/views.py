import json
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models import Sum, Count
from dashboard.models import Operation, Account
from .forms import SignUpForm
from dashboard.currency_converter import convert_to_brl


def get_equity_curve_data_for_echarts(user_id):
    operations = Operation.objects.filter(
        user_id=user_id, status='FECHADA', end_date__isnull=False
    ).order_by('end_date')

    if not operations.exists():
        return {'dates': [], 'values': []}

    converted_data = []
    for op in operations:
        converted_result = convert_to_brl(
            op.net_financial_result, op.account.currency, op.end_date)
        if converted_result is not None:
            converted_data.append({
                'end_date': op.end_date.strftime('%Y-%m-%d'),
                'converted_result': converted_result
            })

    if not converted_data:
        return {'dates': [], 'values': []}

    df = pd.DataFrame(converted_data)
    df['resultado_acumulado'] = df['converted_result'].cumsum()

    return {
        'dates': list(df['end_date']),
        'values': [round(float(v), 2) for v in df['resultado_acumulado']]
    }


@login_required
def home(request):
    operations = Operation.objects.filter(user=request.user)
    closed_operations = operations.filter(
        status='FECHADA', end_date__isnull=False)
    total_pl_converted = sum(convert_to_brl(op.net_financial_result, op.account.currency, op.end_date)
                             for op in closed_operations if op.net_financial_result is not None)
    trade_count = closed_operations.count()
    winning_trades = closed_operations.filter(
        net_financial_result__gt=0).count()
    win_rate = (winning_trades / trade_count * 100) if trade_count > 0 else 0

    chart_data = get_equity_curve_data_for_echarts(request.user.id)

    context = {
        'operations': operations.order_by('-start_date'),
        'total_pl': total_pl_converted,
        'trade_count': trade_count,
        'win_rate': win_rate,
        # Passamos o dicionário Python diretamente para o template
        'chart_data': chart_data
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
