from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ADICIONE ESTA LINHA:
    # Ela conecta as URLs internas que o django-plotly-dash precisa para funcionar.
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

    # A rota para o nosso app 'core' continua a mesma
    path('', include('core.urls', namespace='core')),
]
