# Em core/urls.py (crie este arquivo se não existir)

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    # Rota da nossa página inicial
    path('', views.home, name='home'),

    # --- ROTAS DE AUTENTICAÇÃO ---
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.register, name='register'),
]
