from django.shortcuts import render,redirect,get_list_or_404
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
    return render(request,'Inicio/inicio.html')
