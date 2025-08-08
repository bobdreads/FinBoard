from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

    # Rota para o app 'core'
    path('', include('core.urls', namespace='core')),

    # ADICIONE ESTA LINHA:
    # Conecta as URLs do app dashboard ao nosso projeto
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]
