import json
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth import login
from django.db.models import Sum, Count
from dashboard.models import Operation, Account
from .forms import SignUpForm
from dashboard.currency_converter import convert_to_brl
from collections import defaultdict


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
    """
    Renderiza o dashboard principal com KPIs dinâmicos e gráficos interativos.
    """
    today = timezone.localtime(timezone.now()).date()
    user_accounts = Account.objects.filter(user=request.user, is_active=True)
    all_closed_ops = Operation.objects.filter(
        user=request.user, status='FECHADA', end_date__isnull=False)
    total_pl_converted = sum(convert_to_brl(op.net_financial_result, op.account.currency, op.end_date)
                             for op in all_closed_ops if op.net_financial_result is not None)

    # --- 1. CÁLCULO DO PATRIMÔNIO TOTAL (SALDO) ---
    total_initial_balance = sum(acc.initial_balance for acc in user_accounts)
    total_current_balance = sum(acc.current_balance for acc in user_accounts)

    patrimony_change_percentage = 0
    if total_initial_balance > 0:
        patrimony_change_percentage = (
            (total_current_balance / total_initial_balance) - 1) * 100

    # --- 2. CÁLCULO DOS GANHOS EM PERÍODOS ---
    # Ganhos no último dia de operação
    last_op_day = all_closed_ops.order_by('-end_date').first()
    gains_last_day = 0
    if last_op_day:
        last_day_ops = all_closed_ops.filter(
            end_date__date=last_op_day.end_date.date())
        gains_last_day = sum(convert_to_brl(op.net_financial_result, op.account.currency,
                             op.end_date) for op in last_day_ops if op.net_financial_result)

    # Ganhos no Mês Atual
    month_ops = all_closed_ops.filter(
        end_date__year=today.year, end_date__month=today.month)
    gains_this_month = sum(convert_to_brl(op.net_financial_result, op.account.currency,
                           op.end_date) for op in month_ops if op.net_financial_result)

    # Ganhos no Ano Atual
    year_ops = all_closed_ops.filter(end_date__year=today.year)
    gains_this_year = sum(convert_to_brl(op.net_financial_result, op.account.currency,
                          op.end_date) for op in year_ops if op.net_financial_result)

    # --- 3. CÁLCULO DOS PERCENTUAIS RELATIVOS AO SALDO ---
    last_day_percentage = (
        gains_last_day / total_current_balance * 100) if total_current_balance > 0 else 0
    month_percentage = (gains_this_month / total_current_balance *
                        100) if total_current_balance > 0 else 0
    year_percentage = (gains_this_year / total_current_balance *
                       100) if total_current_balance > 0 else 0

    # --- KPIs existentes ---
    trade_count = all_closed_ops.count()
    # Este cálculo é simplificado, não considera conversão
    winning_trades = all_closed_ops.filter(net_financial_result__gt=0).count()
    losing_trades = all_closed_ops.filter(net_financial_result__lt=0).count()
    win_rate = (winning_trades / trade_count * 100) if trade_count > 0 else 0

    # --- Dados para os Gráficos (sem alterações) ---
    chart_data = get_equity_curve_data_for_echarts(request.user.id)

    context = {
        'operations': Operation.objects.filter(user=request.user).order_by('-start_date'),
        'total_current_balance': total_current_balance,
        'patrimony_change_percentage': patrimony_change_percentage,
        'gains_last_day': gains_last_day,
        'last_day_percentage': last_day_percentage,
        'gains_this_month': gains_this_month,
        'month_percentage': month_percentage,
        'gains_this_year': gains_this_year,
        'year_percentage': year_percentage,
        'trade_count': trade_count,
        'win_rate': win_rate,
        'winning_trades': winning_trades,  # Adiciona ao contexto
        'losing_trades': losing_trades,
        'chart_data': chart_data,
        'total_pl': total_pl_converted,

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
