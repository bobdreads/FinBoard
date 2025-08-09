from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory  # Importe o inlineformset_factory
from django.db import transaction

from decimal import Decimal

from .models import Account, Transaction, Operation, Strategy, Movement
from .forms import AccountForm, TransactionForm, OperationForm, StrategyForm, MovementForm


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
            try:
                # Usamos uma transação atômica para garantir que ou tudo é salvo, ou nada é.
                with transaction.atomic():
                    operation = form.save(commit=False)
                    operation.user = request.user
                    operation.save()
                    form.save_m2m()  # Salva as tags

                    # Agora, salvamos os movimentos associando-os à operação recém-criada
                    formset.instance = operation
                    formset.save()

                    return redirect('core:home')
            except IntegrityError:
                # Lidar com possíveis erros aqui
                print("Erro ao salvar form/formset.")
    else:
        form = OperationForm(user=request.user)
        formset = MovementFormSet()

    context = {
        'form': form,
        'formset': formset,  # Passamos o formset para o template
    }
    return render(request, 'dashboard/operation_form.html', context)


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
