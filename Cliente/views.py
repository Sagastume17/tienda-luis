from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Cliente
from .form import ClienteForm
from django.utils import timezone

@login_required
def cliente_list(request):
    clientes = Cliente.objects.all().order_by('nit')
    paginator = Paginator(clientes, 10)  # 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Cliente/lista.html', {'page_obj': page_obj})


@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            nit = form.cleaned_data.get('nit')  # 👀 obtenemos el NIT del formulario
            # Verificar si ya existe un cliente con ese NIT
            if Cliente.objects.filter(nit__iexact=nit).exists():
                messages.warning(request, f'El cliente con NIT "{nit}" ya está registrado.')
                return render(request, 'Cliente/nuevo.html', {'form': form})
            
            try:
                c = form.save(commit=False)
                c.compra = 0
                c.total = 0.00
                c.usuario = request.user
                c.save()
                messages.success(request, f'Cliente {c.nombre} ingresado correctamente!')
                return redirect('NuevoClie')
            except Exception as e:
                messages.error(request, f'Error al ingresar Cliente: {str(e)}')
                return render(request, 'Cliente/nuevo.html', {'form': form})
        else:
            # Si el formulario no es válido, se vuelve a mostrar con errores
            return render(request, 'Cliente/nuevo.html', {'form': form})
    else:
        form = ClienteForm()
        return render(request, 'Cliente/nuevo.html', {'form': form})


@login_required 
def cliente_detail(request, pk): 
    cliente = get_object_or_404(Cliente, pk=pk) 
    return render(request, 'Cliente/detalle.html', {'cliente': cliente})

@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('ListaCli')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'Cliente/nuevo.html', {'form': form, 'accion': 'Editar Cliente'})

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('ListaCli')
    return render(request, 'Cliente/delete.html', {'cliente': cliente})
