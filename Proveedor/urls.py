from . import views
from django.urls import path


urlpatterns = [
    path('nuevo-proveedor/',views.nuevo,name="NuevoProv"),
    path('listado-proveedores/',views.listado,name="ListaProv"),
    path('modificar-proveedor/<int:t>',views.update,name="UpdateProv"),
    path('baja-proveedor/<int:t>',views.baja,name="BajaProv"),
    path('alta-proveedor/<int:t>',views.alta,name="AltaProv"),
]
