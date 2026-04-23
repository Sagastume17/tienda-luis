from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('nuevo-producto/',views.nuevo,name="NuevoProd"),
    path('listado-productos/',views.listado,name="ListaProd"),
    path('listado-productos-2/',views.listado2,name="ListaProd2"),
    path('modificar-producto/<int:t>',views.update,name="UpdateProd"),
    path('inversion-productos/',views.reporte_inversion,name="InvesionProd"),
    path('baja-producto/<int:t>',views.baja,name="BajaProd"),
    path('alta-producto/<int:t>',views.alta,name="AltaProd"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)