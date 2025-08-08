from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # A primeira rota que estamos criando: a lista de contas
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.account_create, name='account_add'),
]
