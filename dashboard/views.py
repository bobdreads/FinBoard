from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.forms import inlineformset_factory
from django.db import transaction, IntegrityError
from django.db.models import Sum, Count, Avg, Max, Min, F, ExpressionWrapper, fields
from django.utils import timezone
from datetime import datetime, timedelta

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
    Exibe os detalhes de uma conta específica, incluindo seu histórico de transações com saldo corrente.
    """
    account = get_object_or_404(Account, pk=pk, user=request.user)

    # Busca as transações em ordem cronológica para o cálculo
    transactions_list = list(account.transactions.order_by('date', 'pk'))

    # Calcula o saldo corrente
    balance = account.initial_balance
    for tx in transactions_list:
        if tx.type == 'DEPOSITO':
            balance += tx.amount
        elif tx.type == 'SAQUE':
            balance -= tx.amount
        tx.running_balance = balance  # Atribui o saldo calculado ao objeto

    # Inverte a lista para exibir a mais recente primeiro
    transactions_list.reverse()

    context = {
        'account': account,
        'transactions': transactions_list,
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
    Atualiza uma operação existente e seus movimentos.
    """
    operation = get_object_or_404(Operation, pk=pk, user=request.user)

    MovementFormSet = inlineformset_factory(
        Operation,
        Movement,
        form=MovementForm,
        extra=0,  # CORREÇÃO: Não adicionar formulários extras ao editar
        can_delete=True  # Permite que o usuário marque movimentos para exclusão
    )

    if request.method == 'POST':
        form = OperationForm(
            request.POST, instance=operation, user=request.user)
        formset = MovementFormSet(request.POST, instance=operation)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    formset.save()
                    # A lógica de recálculo no model Movement cuidará de atualizar o status
                    operation.update_calculated_fields()
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
    # Usaremos o mesmo template do formulário de criação, mas o contexto o adaptará
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
    Exibe um resumo de performance para um dia específico.
    """
    # Pega a data do request (via GET), ou usa a data de hoje como padrão
    date_str = request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Filtra operações fechadas NAQUELE DIA para o usuário logado
    daily_ops = Operation.objects.filter(
        user=request.user,
        status='FECHADA',
        end_date__date=selected_date
    ).order_by('end_date')

    # --- 1. CÁLCULO DOS KPIs ---
    total_time_in_trades = timedelta()
    max_drawdown = 0

    # --- CÁLCULO DOS KPIs ---
    daily_results_brl = [convert_to_brl(op.net_financial_result, op.account.currency, op.end_date)
                         for op in daily_ops if op.net_financial_result is not None]

    # P/L Diário (com conversão de moeda)
    total_pl_day = sum(convert_to_brl(op.net_financial_result, op.account.currency, op.end_date)
                       for op in daily_ops if op.net_financial_result is not None)

    # Número de trades
    trade_count_day = daily_ops.count()

    # Taxa de Acerto
    winning_trades_day = daily_ops.filter(net_financial_result__gt=0).count()
    win_rate_day = (winning_trades_day / trade_count_day *
                    100) if trade_count_day > 0 else 0

    # Expectativa Matemática (Resultado Médio por trade)
    # Precisamos converter cada resultado antes de calcular a média
    daily_results_brl = [convert_to_brl(op.net_financial_result, op.account.currency, op.end_date)
                         for op in daily_ops if op.net_financial_result is not None]
    avg_result_day = sum(daily_results_brl) / \
        len(daily_results_brl) if daily_results_brl else 0

    avg_result_day = round(avg_result_day, 2)

    # 2. Drawdown Máximo do Dia (em BRL)
    if daily_ops.exists():
        # 1. Tempo Total Operando
        for op in daily_ops:
            if op.end_date and op.start_date:
                total_time_in_trades += op.end_date - op.start_date

        # 2. Drawdown Máximo do Dia (em BRL)
        peak = 0
        cumulative_pl = 0
        for result in daily_results_brl:
            cumulative_pl += result
            if cumulative_pl > peak:
                peak = cumulative_pl

            drawdown = peak - cumulative_pl
            if drawdown > max_drawdown:
                max_drawdown = drawdown

    context = {
        'selected_date': selected_date,
        'date_str': date_str,  # Para preencher o seletor de data
        'daily_ops': daily_ops,
        'total_pl_day': total_pl_day,
        'trade_count_day': trade_count_day,
        'win_rate_day': win_rate_day,
        'avg_result_day': avg_result_day,
        'total_time_in_trades': total_time_in_trades,
        'max_drawdown': max_drawdown,
    }

    return render(request, 'dashboard/daily_summary.html', context)
