from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('coordenadores/', include('coordenador.urls')),
    path('candidatos/', include('candidato.urls')),
    path('lideranca/', include('lideranca.urls', namespace='lideranca')),
    path('pesquisa/', include('pesquisa.urls')),  # Incluindo URLs do app pesquisa

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

