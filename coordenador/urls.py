# coordenador/urls.py
from django.urls import path
from . import views

app_name = 'coordenador'

urlpatterns = [
    path('principal1/', views.coordenador_main, name='coordenador_main'),
    path('cordenadores', views.coordenador_list, name='coordenador_list'),
    path('novo/', views.coordenador_create, name='coordenador_create'),
    path('<int:pk>/editar/', views.coordenador_update, name='coordenador_edit'),  # URL para edição
    #path('<int:pk>/deletar/', views.coordenador_delete, name='coordenador_delete'),  # URL para exclusão (se necessário)
]
