from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Qualquer requisição para a raiz do site ('') será redirecionada
    # para as URLs definidas no arquivo 'core.urls'.
    path('', include('core.urls', namespace='core')),
]
