from django.urls import path
from . import views

app_name = 'lideranca'

urlpatterns = [
    path('', views.lideranca_list, name='lideranca_list'),
    path('create/', views.lideranca_create, name='lideranca_create'),
    path('edit/<int:pk>/', views.lideranca_edit, name='lideranca_edit'),
    path('contato/', views.contato_list, name='contato_list'),
    path('contato/create/', views.contato_create, name='contato_create'),
    path('contato/edit/<int:pk>/', views.contato_edit, name='contato_edit'),
    path('relatorio-aniversariantes/', views.relatorio_aniversariantes, name='relatorio_aniversariantes'),
]
