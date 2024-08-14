from django.urls import path
from . import views
from .views import generate_qr_code


app_name = 'lideranca'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('principal1/<int:lideranca_id>/', views.lideranca_main, name='lideranca_main'),
    path('', views.lideranca_list, name='lideranca_list'),
    path('create/', views.lideranca_create, name='lideranca_create'),
    path('edit/<int:pk>/', views.lideranca_edit, name='lideranca_edit'),
    path('contato/', views.contato_list, name='contato_list'),
    path('contato/create/', views.contato_create, name='contato_create'),
    path('contato/edit/<int:pk>/', views.contato_edit, name='contato_edit'),
    path('relatorio-aniversariantes/', views.relatorio_aniversariantes, name='relatorio_aniversariantes'),
    path('relatorio-cadastros/', views.relatorio_cadastros, name='relatorio_cadastros'),
    path('generate_qr_code/', generate_qr_code, name='generate_qr_code'),

]
