from user import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('nuevousuario/',views.nuevousuario,name="NuevoUser"),
    path('listausuario/',views.listausuario,name="ListaUser"),
    path('listausuario2/',views.listausuario2,name="ListaUser2"),
    path('updateusuario/<str:id>',views.updateusuario,name="UpdateUser"),
    path('updatepass/<int:id>',views.updatepass,name="UpdatePass"),
    path('bajausuario/<int:id>',views.baja,name="BajaUser"),
     path('altausuario/<int:id>',views.alta,name="AltaUser"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)