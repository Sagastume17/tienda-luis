from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Abastecer,Detalle
from Producto.models import Producto
from Proveedor.models import Proveedor
from .form import AbastecerForm,UpdateAbastecerForm,DetalleForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q,Sum,F,ExpressionWrapper,DecimalField
from decimal import Decimal


@login_required
def nuevo(request):
    if request.method == 'POST':
        form = AbastecerForm(request.POST)
        if form.is_valid():
            try:
                p = form.save(commit=False)
                p.estado = 0
                p.fecha = timezone.now()
                p.usuario = request.user
                p.save()
                messages.success(request, f'Inicio de Abastecimiento!')
                return redirect('DetalleAbas',p.id)
            except Exception as e:
                messages.error(request, f'Error al ingresar abastecimiento: {str(e)}')
                return redirect('NuevoAbas')
    else:
        form = AbastecerForm()

    return render(request, 'Abastecer/nuevo.html', {'form': form})



@login_required
def detalle(request, t):
    abastecer = get_object_or_404(Abastecer, id=t)
    det = Detalle.objects.filter(abastecedor_id=t)
    tok = False 
    


    qs = Detalle.objects.filter(abastecedor_id=t).annotate(
        producto=ExpressionWrapper(
            F("compra_ahora") * F("ingreso_ahora"),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        )
        )

    van = qs.aggregate(total=Sum("producto"))["total"] or Decimal("0.00")

    # Comparar con abastecer.total usando tolerancia
    if abs(van - abastecer.total) < Decimal("0.01"):
        vv = True
    else:
        vv = False

    
    buscar = request.POST.get('buscar', '').strip()
    if request.method == 'POST': 
        
        if 'buscar' in request.POST:    
            if not buscar: 
                messages.error(request, 'Campo Busqueda No Puede Estar Vacio') 
                return redirect('DetalleAbas', t)
            else:
                querys = (Q(codigo__icontains=request.POST['buscar'].strip()) | 
                          Q(nombre__icontains=request.POST['buscar'].strip()))
                busqueda = Producto.objects.filter(querys)
                return render(
                    request,
                    'Abastecer/detalle.html',
                    {
                        'a': abastecer,
                        'tok': True,
                        'b': busqueda,
                        'form': DetalleForm(),
                        'd': det,
                        'vv': vv,
                        'van':van,
                    }
                )
        
        elif 'agregar' in request.POST: 
            form = DetalleForm(request.POST)
            id_prod = request.POST.get('id_prod') 
            
            if not id_prod: 
                messages.error(request, 'No se recibió el producto') 
                return redirect('DetalleAbas', t) 
            
            p = get_object_or_404(Producto, pk=int(id_prod))
            proveedor = get_object_or_404(Proveedor, nit=abastecer.proveedor)
            
            if form.is_valid(): 
                venta = form.cleaned_data.get('venta_ahora', 0) 
                compra = form.cleaned_data.get('compra_ahora', 0) 
                ingreso = form.cleaned_data.get('ingreso_ahora', 0) 
                
                if any(val > 0 for val in [venta, compra, ingreso]): 
                    a = form.save(commit=False)
                    a.abastecedor_id = t
                    a.prod_id = id_prod
                    a.venta_antes = p.venta
                    a.compra_antes = p.compra
                    a.ingreso_antes = p.ingreso
                    a.usuario = request.user
                    a.fecha = timezone.now()
                    a.save()
                    
                    p.compra = form.cleaned_data['compra_ahora']
                    p.venta = form.cleaned_data['venta_ahora']
                    p.ingreso += form.cleaned_data['ingreso_ahora']
                    p.abastecedor_id = t
                    p.prod_id = id_prod
                    p.save()
                    
                    proveedor.compras += 1
                    proveedor.total += (
                        form.cleaned_data['compra_ahora'] *
                        form.cleaned_data['ingreso_ahora']
                    )
                    proveedor.fecha = timezone.now()
                    proveedor.save()
                    
                    messages.success(request, 'Agregado!') 
                    return redirect('DetalleAbas', t) 
                else: 
                    messages.error(request, 'Uno de los valores debe ser mayor a 0!') 
                    return redirect('DetalleAbas', t)
        
        elif 'quitar' in request.POST: 
            id_detalle = request.POST['id_detalle'] 
            ab = get_object_or_404(Detalle, id=int(id_detalle))
            pr = get_object_or_404(Producto, id=int(ab.prod.pk))
            prov = get_object_or_404(Proveedor, nit=abastecer.proveedor)
            
            pr.ingreso -= ab.ingreso_ahora 
            pr.save() 
            
            prov.compras -= 1
            prov.total -= (ab.compra_ahora * ab.ingreso_ahora)
            prov.save()
            
            ab.delete()
            messages.success(request, f'{pr.nombre} Quitado de Abastecimiento!')
            return redirect('DetalleAbas', t)
            
        else:
            abastecer.estado = 1
            abastecer.save()
            messages.success(request, f'Abastecimiento Terminado!')
            return redirect('NuevoAbas')                
            
    else:
        return render(
            request,
            'Abastecer/detalle.html',
            {
                'form': DetalleForm(),
                'tok': tok,
                'd': det,
                'a': abastecer,
                'vv': vv,
                'van':van,
            }
        )



@login_required
def listado_abastecimiento(request):
    # Traer todos los detalles de abastecimiento ordenados por fecha
    detalles = Detalle.objects.all().order_by('-fecha')

    # Paginación: 10 registros por página
    paginator = Paginator(detalles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Abastecer/lista.html', {
        'page_obj': page_obj
    })

@login_required
def historial_abastecimiento(request, prod_id):
    # Historial de un producto específico
    producto = get_object_or_404(Producto, pk=prod_id)
    historial = Detalle.objects.filter(prod=producto).order_by('-fecha')

    paginator = Paginator(historial, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Abastecer/historial.html', {
        'producto': producto,
        'page_obj': page_obj
    })



@login_required
def update(request,t): 
    abastecer = get_object_or_404(Abastecer, id=t) 
    form = UpdateAbastecerForm(instance=abastecer)
    if request.method == 'POST': 
        form = UpdateAbastecerForm(request.POST, instance=abastecer) 
        if form.is_valid(): 
            form.save() 
            messages.success(request, "Abastecimiento actualizado correctamente.") 
            return redirect('ListaAbas') 
        else:
            messages.error(request, "Abastecimiento NO actualizado") 
            return redirect('ListaAbas')  
             
    
    return render(request, 'Abastecer/update.html', {'form': form})


@login_required
def baja(request,t):
    abastecer = get_object_or_404(Abastecer, id=t) 
    abastecer.estado=2
    abastecer.save()
    messages.success(request, "Abasteciemto dado de baja correctamente.") 
    return redirect('ListaAbas')
 
    
@login_required
def alta(request,t):
    abastecer = get_object_or_404(Abastecer, id=t) 
    abastecer.estado=1
    abastecer.save()
    messages.success(request, "Abastecimiento dado de alta correctamente.") 
    return redirect('ListaAbas')      