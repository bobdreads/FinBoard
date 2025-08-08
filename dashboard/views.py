from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import AccountForm


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
            return redirect('dashboard:account_list')
    else:
        # Se for um GET, apenas exiba um formulário em branco
        form = AccountForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/account_form.html', context)
