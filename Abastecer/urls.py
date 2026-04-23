from . import views
from django.urls import path


urlpatterns = [
    path('nuevo-abastecer/',views.nuevo,name="NuevoAbas"),
    path('detalle-abastecer/<int:t>',views.detalle,name="DetalleAbas"),
    path('listado-abastecimientos/', views.listado_abastecimiento, name='ListaAbas'), 
    path('historial-abastecimiento/<int:prod_id>/', views.historial_abastecimiento, name='HistorialAbas'),
    path('modificar-abastecimiento/<int:t>',views.update,name="UpdateAbas"),
    path('baja-abastecer/<int:t>',views.baja,name="BajaAbas"),
    path('alta-abastecer/<int:t>',views.alta,name="AltaAbas"),
]
