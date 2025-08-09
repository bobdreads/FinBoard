from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('', include('core.urls', namespace='core')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]
