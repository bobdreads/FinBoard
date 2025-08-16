import json
import numpy as np

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.db import transaction, IntegrityError
from django.db.models import Sum, Count, Avg, Max, Min, F, ExpressionWrapper, fields
from django.db.models.functions import TruncHour
from django.utils import timezone

from decimal import Decimal
from datetime import datetime, timedelta
from collections import defaultdict

from .models import Account, Transaction, Operation, Strategy, Movement
from .forms import AccountForm, TransactionForm, OperationForm, StrategyForm, MovementForm
from .currency_converter import convert_to_brl


@login_required
def account_list(request):
    """
    Esta view exibe a lista de contas (carteiras) do usuário logado.
    """
    accounts = Account.objects.filter(user=request.user).order_by('name')

    context = {
        'accounts': accounts
    }
    return render(request, 'dashboard/account_list.html', context)


@login_required
def account_create(request):
    """
    View para criar uma nova conta (carteira).
    """
    if request.method == 'POST':
        # Se o formulário foi enviado, crie uma instância com os dados
        form = AccountForm(request.POST)
        if form.is_valid():
            # Antes de salvar, associe a nova conta ao usuário logado
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            # Redirecione o usuário de volta para a lista de carteiras
            return render(request, 'dashboard/account_form.html', context)
    else:
        # Se for um GET, apenas exiba um formulário em branco
        form = AccountForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/account_form.html', context)


@login_required
def account_detail(request, pk):
    """
    Exibe o histórico de transações de uma conta com o saldo corrente
    calculado corretamente, incluindo os resultados das operações.
    """
    account = get_object_or_404(Account, pk=pk, user=request.user)

    # 1. Coleta todos os eventos financeiros da conta
    transactions = account.transactions.all()
    closed_ops = account.operation_set.filter(
        status='FECHADA', end_date__isnull=False)

    # Cria uma lista unificada de eventos para cálculo
    all_events = []
    for t in transactions:
        all_events.append({
            'date': t.date,
            'amount': t.amount if t.type == 'DEPOSITO' else -t.amount,
            'is_transaction': True,  # Marca que este evento é uma transação
            'object': t  # Guarda o objeto original da transação
        })

    for op in closed_ops:
        if op.net_financial_result is not None:
            all_events.append({
                'date': op.end_date,
                'amount': op.net_financial_result,
                'is_transaction': False  # Marca que não é uma transação
            })

    # 2. Ordena todos os eventos cronologicamente
    all_events.sort(key=lambda x: x['date'])

    # 3. Calcula o saldo corrente para cada evento e armazena nas transações
    running_balance = account.initial_balance
    transactions_with_balance = []

    for event in all_events:
        running_balance += event['amount']
        # Se o evento for uma transação, nós guardamos o saldo calculado
        if event['is_transaction']:
            transaction_obj = event['object']
            transaction_obj.running_balance = running_balance  # Anexa o saldo ao objeto
            transactions_with_balance.append(transaction_obj)

    # A lista `transactions_with_balance` agora contém apenas as transações,
    # mas cada uma tem um novo atributo `.running_balance` com o valor correto.

    # Inverte a lista para exibir a mais recente primeiro
    transactions_with_balance.reverse()

    context = {
        'account': account,
        'transactions': transactions_with_balance,
    }
    return render(request, 'dashboard/account_detail.html', context)


@login_required
def transaction_create(request, account_pk):
    """
    Cria uma nova transação (depósito ou saque) para uma conta específica.
    """
    # Garante que a conta pertence ao usuário logado
    account = get_object_or_404(Account, pk=account_pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account  # Associa a transação à conta correta
            transaction.save()
            # Redireciona para a página de detalhes da conta
            return redirect('dashboard:account_detail', pk=account.pk)
    else:
        form = TransactionForm()

    context = {
        'form': form,
        'account': account
    }
    return render(request, 'dashboard/transaction_form.html', context)


@login_required
def operation_create(request):
    """
    Cria uma nova operação (trade).
    """
    MovementFormSet = inlineformset_factory(
        Operation,
        Movement,
        form=MovementForm,
        # Começamos com 2 formulários de movimento (1 entrada, 1 saída)
        extra=2,
        can_delete=False
    )

    if request.method == 'POST':
        form = OperationForm(request.POST, user=request.user)
        formset = MovementFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # --- LÓGICA DE CORREÇÃO ---
            # 1. Extrair a data de início antes de salvar
            earliest_date = None

            # Filtra os formulários de movimento que foram realmente preenchidos
            valid_movements_data = [
                f.cleaned_data for f in formset if f.has_changed()]

            if not valid_movements_data:
                form.add_error(
                    None, "Você deve preencher pelo menos um movimento.")
            else:
                # Encontra a menor data entre os movimentos preenchidos
                earliest_date = min(
                    data['datetime'] for data in valid_movements_data if data.get('datetime'))

            if earliest_date:
                try:
                    with transaction.atomic():
                        operation = form.save(commit=False)
                        operation.user = request.user

                        # 2. Atribuir a data de início ANTES de salvar a operação
                        operation.start_date = earliest_date

                        operation.save()
                        form.save_m2m()  # Salva as tags

                        formset.instance = operation
                        formset.save()

                        return redirect('core:home')
                except IntegrityError as e:
                    print(f"Erro de Integridade: {e}")
        else:
            print("Erros de Validação:", form.errors, formset.errors)
    else:
        form = OperationForm(user=request.user)
        formset = MovementFormSet()

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'dashboard/operation_form.html', context)


@login_required
def operation_list(request):
    """
    Exibe a lista completa de operações do usuário logado.
    """
    operations = Operation.objects.filter(
        user=request.user).order_by('-start_date')
    context = {
        'operations': operations
    }
    return render(request, 'dashboard/operation_list.html', context)


@login_required
def operation_detail(request, pk):
    """
    Exibe todos os detalhes de uma única operação.
    """
    operation = get_object_or_404(Operation, pk=pk, user=request.user)
    movements = operation.movements.all().order_by('datetime')

    context = {
        'operation': operation,
        'movements': movements,
    }
    return render(request, 'dashboard/operation_detail.html', context)


@login_required
def operation_update(request, pk):
    """
    Atualiza uma operação existente e seus movimentos. (VERSÃO CORRIGIDA)
    """
    operation = get_object_or_404(Operation, pk=pk, user=request.user)
    MovementFormSet = inlineformset_factory(
        Operation, Movement, form=MovementForm, extra=0, can_delete=True)

    if request.method == 'POST':
        form = OperationForm(
            request.POST, instance=operation, user=request.user)
        formset = MovementFormSet(request.POST, instance=operation)

        if form.is_valid() and formset.is_valid():
            # --- LÓGICA DE CORREÇÃO ---
            # 1. Pega os dados de todos os movimentos que serão salvos (novos e existentes)
            #    e que не estão marcados para exclusão.
            valid_movements_data = [
                f.cleaned_data for f in formset
                if f.has_changed() and not f.cleaned_data.get('DELETE', False)
            ]

            # Pega os movimentos já existentes que não foram alterados
            existing_movements_data = [
                {'datetime': mov.initial['datetime']} for mov in formset.initial_forms
                if not mov.has_changed() and not mov.cleaned_data.get('DELETE', False)
            ]

            all_movements_data = valid_movements_data + existing_movements_data

            if not all_movements_data:
                form.add_error(
                    None, "Uma operação deve ter pelo menos um movimento.")
            else:
                # 2. Encontra a data mais antiga entre todos os movimentos
                earliest_date = min(
                    data['datetime'] for data in all_movements_data if data.get('datetime'))

                try:
                    with transaction.atomic():
                        # 3. Salva o formulário principal (ainda sem commit)
                        updated_operation = form.save(commit=False)
                        # 4. Atribui a data correta ANTES de salvar no banco
                        updated_operation.start_date = earliest_date
                        updated_operation.save()
                        form.save_m2m()

                        # 5. Salva os movimentos
                        formset.instance = updated_operation
                        formset.save()

                        # A lógica de recálculo no model Movement cuidará de atualizar o status/end_date
                        updated_operation.update_calculated_fields()

                        return redirect('dashboard:operation_detail', pk=operation.pk)
                except IntegrityError as e:
                    print(f"Erro de Integridade na atualização: {e}")
        else:
            print("Erros de Validação:", form.errors, formset.errors)
    else:
        form = OperationForm(instance=operation, user=request.user)
        formset = MovementFormSet(instance=operation)

    context = {
        'form': form,
        'formset': formset,
        'operation': operation,
    }
    return render(request, 'dashboard/operation_form.html', context)


@login_required
def operation_delete(request, pk):
    """
    Exclui uma operação após a confirmação do usuário.
    """
    operation = get_object_or_404(Operation, pk=pk, user=request.user)
    if request.method == 'POST':
        operation.delete()
        # Após deletar, envia o usuário para a lista de operações
        return redirect('dashboard:operation_list')

    context = {
        'operation': operation
    }
    return render(request, 'dashboard/operation_confirm_delete.html', context)


@login_required
def strategy_list(request):
    # No futuro, podemos filtrar por usuário se necessário
    strategies = Strategy.objects.all()
    return render(request, 'dashboard/strategy_list.html', {'strategies': strategies})


@login_required
def strategy_create(request):
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:strategy_list')
    else:
        form = StrategyForm()
    return render(request, 'dashboard/strategy_form.html', {'form': form, 'action': 'Adicionar'})


@login_required
def strategy_update(request, pk):
    strategy = get_object_or_404(Strategy, pk=pk)
    if request.method == 'POST':
        form = StrategyForm(request.POST, instance=strategy)
        if form.is_valid():
            form.save()
            return redirect('dashboard:strategy_list')
    else:
        form = StrategyForm(instance=strategy)
    return render(request, 'dashboard/strategy_form.html', {'form': form, 'action': 'Editar'})


@login_required
def strategy_delete(request, pk):
    strategy = get_object_or_404(Strategy, pk=pk)
    if request.method == 'POST':
        strategy.delete()
        return redirect('dashboard:strategy_list')
    return render(request, 'dashboard/strategy_confirm_delete.html', {'object': strategy})


@login_required
def daily_summary(request):
    """
    Exibe um resumo de performance para um período de tempo selecionado. (VERSÃO CORRIGIDA E REATORADA)
    """
    today = timezone.localtime(timezone.now()).date()

    # --- 1. LÓGICA DE DATAS CENTRALIZADA ---
    # Garante que as datas estejam sempre na URL, buscando da sessão se necessário.
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str or not end_date_str:
        start_date_s = request.session.get(
            'summary_start_date', today.strftime('%Y-%m-%d'))
        end_date_s = request.session.get(
            'summary_end_date', today.strftime('%Y-%m-%d'))
        return redirect(f"{request.path}?start_date={start_date_s}&end_date={end_date_s}")

    # Salva as datas válidas na sessão para persistência
    request.session['summary_start_date'] = start_date_str
    request.session['summary_end_date'] = end_date_str

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # --- 2. QUERYSET PRINCIPAL ---
    # Todas as métricas usarão este mesmo queryset para consistência.
    period_ops = Operation.objects.filter(
        user=request.user,
        status='FECHADA',
        end_date__date__range=[start_date, end_date]
    ).select_related('strategy', 'asset', 'account').order_by('end_date')

    # --- 3. CÁLCULOS DE KPI (usando period_ops) ---
    raw_results = [convert_to_brl(op.net_financial_result, op.account.currency, op.end_date)
                   for op in period_ops if op.net_financial_result is not None]

    # (O restante da sua lógica de KPI continua aqui, sem alterações)
    total_pl_period = sum(raw_results)
    trade_count_period = period_ops.count()
    winning_trades_period = len([r for r in raw_results if r > 0])
    win_rate_period = (winning_trades_period /
                       trade_count_period * 100) if trade_count_period > 0 else 0
    avg_result_period = round(
        sum(raw_results) / len(raw_results) if raw_results else 0, 2)
    max_gain = max(raw_results) if raw_results else 0
    max_loss = min(raw_results) if raw_results else 0

    total_time_in_trades = timedelta()
    if period_ops.exists():
        for op in period_ops:
            if op.end_date and op.start_date:
                total_time_in_trades += op.end_date - op.start_date

    peak = 0
    cumulative_pl = 0
    max_drawdown = 0
    for result in raw_results:
        cumulative_pl += result
        if cumulative_pl > peak:
            peak = cumulative_pl
        drawdown = peak - cumulative_pl
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    gains = [r for r in raw_results if r > 0]
    losses = [r for r in raw_results if r < 0]
    avg_gain = round(sum(gains) / len(gains) if gains else 0, 2)
    avg_loss = round(sum(losses) / len(losses) if losses else 0, 2)
    risk_reward_ratio = round(abs(avg_gain / avg_loss)
                              if avg_loss != 0 else 0, 2)

    # (Lógicas de performance por estratégia, ativo e direção continuam aqui)
    strategy_performance = defaultdict(
        lambda: {'total_pl': 0, 'trade_count': 0})
    for op in period_ops:
        strategy_name = op.strategy.name if op.strategy else "N/A"
        result_brl = convert_to_brl(
            op.net_financial_result, op.account.currency, op.end_date)
        if result_brl is not None:
            strategy_performance[strategy_name]['total_pl'] += result_brl
            strategy_performance[strategy_name]['trade_count'] += 1

    asset_performance = defaultdict(lambda: {'total_pl': 0, 'trade_count': 0})
    for op in period_ops:
        asset_ticker = op.asset.ticker
        result_brl = convert_to_brl(
            op.net_financial_result, op.account.currency, op.end_date)
        if result_brl is not None:
            asset_performance[asset_ticker]['total_pl'] += result_brl
            asset_performance[asset_ticker]['trade_count'] += 1

    direction_performance = defaultdict(
        lambda: {'total_pl': 0, 'trade_count': 0})
    for op in period_ops:
        direction_name = op.get_initial_operation_type_display()
        result_brl = convert_to_brl(
            op.net_financial_result, op.account.currency, op.end_date)
        if result_brl is not None:
            direction_performance[direction_name]['total_pl'] += result_brl
            direction_performance[direction_name]['trade_count'] += 1

    # --- CÁLCULO PARA O PERÍODO ANTERIOR ---
    period_duration = (end_date - start_date).days + 1
    prev_start_date = start_date - timedelta(days=period_duration)
    prev_end_date = start_date - timedelta(days=1)

    prev_period_ops = Operation.objects.filter(
        user=request.user,
        status='FECHADA',
        end_date__date__range=[prev_start_date, prev_end_date]
    )

    # --- KPIs DO PERÍODO ANTERIOR ---
    prev_period_results_brl = [convert_to_brl(op.net_financial_result, op.account.currency, op.end_date)
                               for op in prev_period_ops if op.net_financial_result is not None]

    total_pl_prev_period = sum(prev_period_results_brl)
    trade_count_prev_period = prev_period_ops.count()
    winning_trades_prev_period = len(
        [r for r in prev_period_results_brl if r > 0])
    win_rate_prev_period = (winning_trades_prev_period /
                            trade_count_prev_period * 100) if trade_count_prev_period > 0 else 0

    # --- CÁLCULO DA VARIAÇÃO PERCENTUAL ---
    def calculate_change(current, previous):
        if previous == 0:
            return float('inf') if current > 0 else 0
        return ((current - previous) / abs(previous)) * 100

    pl_change = calculate_change(total_pl_period, total_pl_prev_period)
    trade_count_change = calculate_change(
        trade_count_period, trade_count_prev_period)
    # Variação de ponto percentual é mais simples
    win_rate_change = win_rate_period - win_rate_prev_period

    # --- DADOS PARA O HISTOGRAMA DE RESULTADOS ---
    period_results_brl = [float(r) for r in raw_results if r is not None]

    histogram_data = {}
    if period_results_brl:
        # Usa a função histogram do NumPy para calcular as faixas (bins) e a contagem
        # Definimos 20 faixas, mas você pode ajustar este número
        counts, bin_edges = np.histogram(period_results_brl, bins=20)

        # Prepara os dados para o ECharts
        bin_labels = []
        for i in range(len(bin_edges) - 1):
            # Cria rótulos legíveis para cada faixa, ex: "R$ 10.00 a R$ 20.00"
            label = f"R$ {bin_edges[i]:.2f} a R$ {bin_edges[i+1]:.2f}"
            bin_labels.append(label)

        histogram_data = {
            'labels': bin_labels,
            'counts': counts.tolist(),  # Converte o array do numpy para uma lista python
        }

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'period_ops': period_ops,
        'total_pl_period': total_pl_period,
        'trade_count_period': trade_count_period,
        'win_rate_period': win_rate_period,
        'avg_result_period': avg_result_period,
        'total_time_in_trades': total_time_in_trades,
        'max_drawdown': max_drawdown,
        'strategy_performance': dict(strategy_performance),
        'max_gain': max_gain,
        'max_loss': max_loss,
        'asset_performance': dict(asset_performance),
        'direction_performance': dict(direction_performance),
        'avg_gain': avg_gain,
        'avg_loss': avg_loss,
        'risk_reward_ratio': risk_reward_ratio,
        'pl_change': pl_change,
        'trade_count_change': trade_count_change,
        'win_rate_change': win_rate_change,
        'histogram_data': json.dumps(histogram_data),
    }

    return render(request, 'dashboard/daily_summary.html', context)
