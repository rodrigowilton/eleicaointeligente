# candidato/urls.py
from django.urls import path
from . import views
from .views import send_whatsapp_message, mark_all_contacts, mark_selected_contacts

app_name = 'candidato'

urlpatterns = [
    path('', views.index, name='index'),  # Index page for candidato
    path('candidatos/', views.candidato_list, name='candidato_list'),
    path('candidato/create/', views.candidato_create, name='candidato_create'),
    path('candidato/edit/<int:pk>/', views.candidato_edit, name='candidato_edit'),
    path('candidato/delete/<int:pk>/', views.candidato_delete, name='candidato_delete'),
    path('metas/', views.meta_list, name='meta_list'),
    path('meta/create/', views.meta_create, name='meta_create'),
    path('meta/edit/<int:pk>/', views.meta_edit, name='meta_edit'),
    path('meta/delete/<int:pk>/', views.meta_delete, name='meta_delete'),
    path('send-whatsapp-message/', send_whatsapp_message, name='send_whatsapp_message'),
    path('mark-all-contacts/', mark_all_contacts, name='mark_all_contacts'),
    path('mark-selected-contacts/', mark_selected_contacts, name='mark_selected_contacts'),
]
