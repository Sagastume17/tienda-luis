from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Proveedor.models import Proveedor
from user.models import User
from .form import ProveedorForm,UpdateProveedorForm
from django.utils import timezone
from django.core.paginator import Paginator


@login_required
def nuevo(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            try:
                p = form.save(commit=False)
                p.compras = 0
                p.total = 0.00
                p.estado = 1
                p.fecha = timezone.now()
                p.usuario = request.user
                p.save()
                messages.success(request, f'Proveedor {p.nombre} ingresado correctamente!')
                return redirect('NuevoProv')
            except Exception as e:
                messages.error(request, f'Error al ingresar proveedor: {str(e)}')
                return redirect('NuevoProv')
    else:
        form = ProveedorForm()
        return render(request, 'Proveedor/nuevo.html', {'form': form})



@login_required
def listado(request):
    proveedor = Proveedor.objects.all().order_by('nit') 
    paginator = Paginator(proveedor, 25) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
    return render(request, "Proveedor/lista.html", {"page_obj": page_obj})


@login_required
def update(request,t): 
    proveedor = get_object_or_404(Proveedor, id=t) 
    form = UpdateProveedorForm(instance=proveedor)
    if request.method == 'POST': 
        form = UpdateProveedorForm(request.POST, instance=proveedor) 
        if form.is_valid(): 
            form.save() 
            messages.success(request, "Proveedor actualizado correctamente.") 
            return redirect('ListaProv') 
        else:
            messages.error(request, "Proveedor NO actualizado") 
            return redirect('ListaProv')  
             
    
    return render(request, 'Proveedor/update.html', {'form': form})


@login_required
def baja(request,t):
    proveedor = get_object_or_404(Proveedor, id=t) 
    proveedor.estado=0
    proveedor.save()
    messages.success(request, "Proveedor dado de baja correctamente.") 
    return redirect('ListaProv')
 
    
@login_required
def alta(request,t):
    proveedor = get_object_or_404(Proveedor, id=t) 
    proveedor.estado=1
    proveedor.save()
    messages.success(request, "Proveedor dado de alta correctamente.") 
    return redirect('ListaProv')      