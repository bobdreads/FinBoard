from django.urls import path
from . import views  # Importa as views do app core

app_name = 'core'  # Boa prática para organizar as URLs

urlpatterns = [
    # Quando a URL estiver "vazia" (ex: http://127.0.0.1:8000/),
    # chame a view 'home'.
    path('', views.home, name='home'),
]
