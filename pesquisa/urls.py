# pesquisa/urls.py

from django.urls import path
from . import views

app_name = 'pesquisa'

urlpatterns = [
    path('', views.pesquisa_create, name='pesquisa_root'),  # Rota raiz
    path('new/', views.pesquisa_create, name='pesquisa_create'),
    path('success/', views.pesquisa_success, name='pesquisa_success'),

]
