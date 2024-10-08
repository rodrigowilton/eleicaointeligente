# candidato/urls.py
from django.urls import path
from . import views
from .views import send_whatsapp_message, mark_all_contacts, mark_selected_contacts
from .views import login_view

app_name = 'candidato'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.index, name='index'),  # Defina sua view para a página principal do candidato

    #path('principal/<intcandidato_id>/', views.candidato_list, name='candidato_list'),
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
    path('status/', views.status_list, name='status_list'),
    path('status/create/', views.status_create, name='status_create'),
    path('status/edit/<int:pk>/', views.status_edit, name='status_edit'),
    path('status/delete/<int:pk>/', views.status_delete, name='status_delete'),
]
