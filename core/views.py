from django.shortcuts import render

# Create your views here.


def home(request):
    """
    Esta view renderiza a página inicial do projeto.
    """
    return render(request, 'core/base.html')
