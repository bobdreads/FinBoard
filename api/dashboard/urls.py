from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [

    path('api/operations/', views.OperationListAPIView.as_view(),
         name='api_operation_list'),
    # A primeira rota que estamos criando: a lista de contas
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.account_create, name='account_add'),
    path('accounts/<int:pk>/', views.account_detail, name='account_detail'),
    path('accounts/<int:account_pk>/add_transaction/',
         views.transaction_create, name='transaction_add'),

    path('operations/add/', views.operation_create, name='operation_add'),
    path('operations/', views.OperationListView.as_view(), name='operation_list'),
    path('operations/<int:pk>/', views.operation_detail, name='operation_detail'),
    path('operations/<int:pk>/edit/',
         views.operation_update, name='operation_edit'),
    path('operations/<int:pk>/delete/',
         views.operation_delete, name='operation_delete'),

    path('strategies/', views.strategy_list, name='strategy_list'),
    path('strategies/add/', views.strategy_create, name='strategy_add'),
    path('strategies/<int:pk>/edit/', views.strategy_update, name='strategy_edit'),
    path('strategies/<int:pk>/delete/',
         views.strategy_delete, name='strategy_delete'),

    path('summary/', views.daily_summary, name='daily_summary'),
]
