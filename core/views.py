from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from dashboard.models import Operation
from .forms import SignUpForm

# Create your views here.


@login_required
def home(request):
    """
    Esta view renderiza a página inicial do projeto.
    """
    operations = Operation.objects.filter(user=request.user)
    context = {
        'operations': operations
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
