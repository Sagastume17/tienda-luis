from django.urls import path
from . import views

urlpatterns = [
    path('lista-clientes/', views.cliente_list, name='ListaCli'),
    path('nuevo-cliente/', views.cliente_create, name='NuevoClie'),
    path('editar-cliente/<int:pk>/', views.cliente_update, name='UpdateCli'),
    path('detalle-cliente/<int:pk>/', views.cliente_detail, name='DetalleCli'),
    path('elimitar-cliente/<int:pk>/', views.cliente_delete, name='DeleteCli'),
]
