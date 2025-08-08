from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm


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
    Exibe os detalhes de uma conta específica, incluindo seu histórico de transações.
    O 'pk' (primary key) é o ID da conta que vem da URL.
    """
    # Usamos get_object_or_404 para buscar a conta. Se não encontrar,
    # ele automaticamente retorna um erro 404 (Página não encontrada).
    # O filtro "user=request.user" garante que um usuário não possa ver a conta de outro.
    account = get_object_or_404(Account, pk=pk, user=request.user)

    # Buscamos todas as transações associadas a esta conta
    transactions = account.transactions.order_by('-date')

    context = {
        'account': account,
        'transactions': transactions,
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
