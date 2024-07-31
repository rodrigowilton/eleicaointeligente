from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('coordenadores/', include('coordenador.urls')),
    path('candidatos/', include('candidato.urls')),
    path('lideranca/', include('lideranca.urls', namespace='lideranca')),
]

