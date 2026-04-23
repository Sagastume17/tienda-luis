from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name='Login'),
    path('Logout/',views.logout_out,name='Salir'),
]
