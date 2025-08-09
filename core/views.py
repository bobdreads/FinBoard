import json
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models import Sum, Count
from dashboard.models import Operation, Account
from .forms import SignUpForm
from dashboard.currency_converter import convert_to_brl
from collections import defaultdict
from datetime import date, timedelta


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


def get_daily_pl_data(user_id):
    """Prepara os dados de Lucro/Prejuízo diário."""
    operations = Operation.objects.filter(
        user_id=user_id, status='FECHADA', end_date__isnull=False
    ).order_by('end_date')

    daily_pl = defaultdict(float)
    for op in operations:
        converted_result = convert_to_brl(
            op.net_financial_result, op.account.currency, op.end_date)
        if converted_result is not None:
            day = op.end_date.strftime('%Y-%m-%d')
            daily_pl[day] += float(converted_result)

    sorted_days = sorted(daily_pl.keys())
    return {
        'dates': sorted_days,
        'values': [round(daily_pl[day], 2) for day in sorted_days]
    }


def get_stacked_accounts_data(user_id):
    """Prepara o histórico de saldo diário para cada conta."""
    accounts = Account.objects.filter(user_id=user_id, is_active=True)
    if not accounts:
        return {'dates': [], 'series': []}

    # Encontra o intervalo de datas geral de todas as operações e transações
    first_date = None
    # (Lógica para encontrar a primeira data pode ser adicionada aqui se necessário)
    # Por simplicidade, vamos usar os últimos 90 dias ou a data do primeiro trade

    # Estrutura final dos dados
    series_data = []
    all_dates_set = set()

    for account in accounts:
        events = []
        # Adiciona o saldo inicial como o primeiro evento
        # (Uma lógica mais robusta encontraria a data do primeiro evento real)

        # Coleta todas as transações e operações da conta
        transactions = account.transactions.all()
        operations = account.operation_set.filter(
            status='FECHADA', end_date__isnull=False)

        for t in transactions:
            amount = t.amount if t.type == 'DEPOSITO' else -t.amount
            events.append({'date': t.date.date(), 'amount': float(amount)})

        for op in operations:
            converted_pl = convert_to_brl(
                op.net_financial_result, account.currency, op.end_date)
            if converted_pl is not None:
                events.append({'date': op.end_date.date(),
                              'amount': float(converted_pl)})

        if not events:
            continue

        # Ordena todos os eventos por data
        events.sort(key=lambda x: x['date'])

        # Gera o histórico de saldo diário
        daily_balance = {}
        current_balance = float(account.initial_balance)
        start_date = events[0]['date']
        end_date = date.today()

        event_idx = 0
        for day_num in range((end_date - start_date).days + 1):
            current_day = start_date + timedelta(days=day_num)
            all_dates_set.add(current_day.strftime('%Y-%m-%d'))

            # Soma os eventos do dia
            while event_idx < len(events) and events[event_idx]['date'] == current_day:
                current_balance += events[event_idx]['amount']
                event_idx += 1
            daily_balance[current_day.strftime(
                '%Y-%m-%d')] = round(current_balance, 2)

        series_data.append({
            'name': account.name,
            'data': daily_balance
        })

    # Preenche os dados para todas as datas
    sorted_dates = sorted(list(all_dates_set))
    final_series = []
    for s in series_data:
        account_data = []
        # Começa com o primeiro saldo conhecido
        last_balance = float(s['data'].get(sorted_dates[0], 0))
        for d in sorted_dates:
            balance = s['data'].get(d, last_balance)
            account_data.append(balance)
            last_balance = balance
        final_series.append({'name': s['name'], 'data': account_data})

    return {'dates': sorted_dates, 'series': final_series}


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

    daily_pl_data = get_daily_pl_data(request.user.id)
    stacked_accounts_data = get_stacked_accounts_data(request.user.id)

    context = {
        'operations': operations.order_by('-start_date'),
        'total_pl': total_pl_converted,
        'trade_count': trade_count,
        'win_rate': win_rate,
        'daily_pl_json': json.dumps(daily_pl_data),
        'stacked_accounts_json': json.dumps(stacked_accounts_data),
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
