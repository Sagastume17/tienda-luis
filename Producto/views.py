from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Producto.models import Producto,Producto2
from user.models import User
from .form import ProductoForm, UpdateProductoForm
from django.core.paginator import Paginator
from django.db.models import Q, F, Sum, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce

@login_required
def nuevo(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            try:
                p = form.save(commit=False)
                p.salida = 0
                p.estado = 1
                p.usuario = request.user
                p.save()
                messages.success(request, f'Producto {p.nombre} ingresado correctamente!')
                return redirect('NuevoProd')
            except Exception as e:
                messages.error(request, f'Error al ingresar producto: {str(e)}')
                return redirect('NuevoProd')
    else:
        form = ProductoForm()

    return render(request, 'Producto/nuevo.html', {'form': form})


from django.db.models import Q, F, Sum, DecimalField, ExpressionWrapper

from django.db.models import Q, Sum, F, DecimalField, ExpressionWrapper
from datetime import datetime
import openpyxl
from django.http import HttpResponse

@login_required
def listado(request):
    query = request.GET.get("q", "")
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    exportar = request.GET.get("exportar")

    productos = Producto.objects.all().order_by("codigo")

    # 🔎 FILTRO POR BUSQUEDA
    if query:
        productos = productos.filter(
            Q(codigo__icontains=query) |
            Q(nombre__icontains=query) |
            Q(categoria__icontains=query)
        )

    # 📅 FILTRO POR FECHA (solo si existe campo fecha)
    if fecha_inicio:
        try:
            productos = productos.filter(fecha__gte=fecha_inicio)
        except:
            pass

    if fecha_fin:
        try:
            productos = productos.filter(fecha__lte=fecha_fin)
        except:
            pass

    # ✅ STOCK Y VALORES
    productos = productos.annotate(
        stock_calc=ExpressionWrapper(
            Coalesce(F('ingreso'), 0) - Coalesce(F('salida'), 0),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        ),
        valor_stock=ExpressionWrapper(
            (Coalesce(F('ingreso'), 0) - Coalesce(F('salida'), 0)) * Coalesce(F('compra'), 0),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        )
    )

    # 📥 EXPORTAR EXCEL
    if exportar:
        return exportar_excel(productos)

    # 💵 DINERO REAL EN INVENTARIO
    stock_invertido = productos.aggregate(
        total=Sum(
            ExpressionWrapper(
                (Coalesce(F('ingreso'), 0) - Coalesce(F('salida'), 0)) * Coalesce(F('compra'), 0),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            )
        )
    )['total'] or 0

    # 📈 GANANCIA REAL
    ganancia = productos.aggregate(
        total=Sum(
            ExpressionWrapper(
                Coalesce(F('salida'), 0) *
                (Coalesce(F('venta'), 0) - Coalesce(F('compra'), 0)),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            )
        )
    )['total'] or 0

    # 💲 VALOR POTENCIAL DE VENTA
    valor_venta_stock = productos.aggregate(
        total=Sum(
            ExpressionWrapper(
                (Coalesce(F('ingreso'), 0) - Coalesce(F('salida'), 0)) * Coalesce(F('venta'), 0),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            )
        )
    )['total'] or 0

    # 📄 PAGINACIÓN
    paginator = Paginator(productos, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "Producto/lista.html", {
        "page_obj": page_obj,
        "query": query,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "stock_invertido": stock_invertido,
        "ganancia": ganancia,
        "valor_venta_stock": valor_venta_stock,
    })

def exportar_excel(productos):
    import openpyxl
    from django.http import HttpResponse

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventario"

    # Encabezados
    ws.append([
        'Código', 'Nombre', 'Categoría',
        'Ingreso', 'Salida', 'Stock',
        'Precio Compra', 'Precio Venta'
    ])

    # Datos
    for p in productos:
        stock = p.ingreso - p.salida

        ws.append([
            p.codigo,
            p.nombre,
            p.categoria,
            p.ingreso,
            p.salida,
            stock,
            float(p.compra),
            float(p.venta),
        ])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="inventario.xlsx"'

    wb.save(response)
    return response



from django.db.models import Q, Sum, F, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def listado2(request):
    query = request.GET.get("q", "")
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    exportar = request.GET.get("exportar")

    productos = Producto2.objects.all().order_by("codigo")

    # 🔎 BÚSQUEDA
    if query:
        productos = productos.filter(
            Q(codigo__icontains=query) |
            Q(nombre__icontains=query) |
            Q(categoria__icontains=query)
        )

    # 📅 FILTRO POR FECHA
    if fecha_inicio:
        try:
            productos = productos.filter(fecha__gte=fecha_inicio)
        except:
            pass

    if fecha_fin:
        try:
            productos = productos.filter(fecha__lte=fecha_fin)
        except:
            pass

    # ✅ STOCK CALCULADO + VALOR
    productos = productos.annotate(
        stock_calc=ExpressionWrapper(
            Coalesce(F('ingreso'), 0) - Coalesce(F('salida'), 0),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        ),
        valor_stock=ExpressionWrapper(
            (Coalesce(F('ingreso'), 0) - Coalesce(F('salida'), 0)) *
            Coalesce(F('compra'), 0),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        )
    )

    # ✅ SOLO PRODUCTOS CON EXISTENCIA
    productos = productos.filter(stock_calc__gt=0)

    # 📥 EXPORTAR EXCEL
    if exportar:
        return exportar_excel_bodega2(productos)

    # 💵 INVENTARIO REAL
    stock_invertido = productos.aggregate(
        total=Sum(
            ExpressionWrapper(
                (Coalesce(F('ingreso'), 0) - Coalesce(F('salida'), 0)) *
                Coalesce(F('compra'), 0),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            )
        )
    )['total'] or 0

    # 📈 GANANCIA
    ganancia = productos.aggregate(
        total=Sum(
            ExpressionWrapper(
                Coalesce(F('salida'), 0) *
                (Coalesce(F('venta'), 0) - Coalesce(F('compra'), 0)),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            )
        )
    )['total'] or 0

    # 💲 VALOR POTENCIAL DE VENTA
    valor_venta_stock = productos.aggregate(
        total=Sum(
            ExpressionWrapper(
                (Coalesce(F('ingreso'), 0) - Coalesce(F('salida'), 0)) *
                Coalesce(F('venta'), 0),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            )
        )
    )['total'] or 0

    # 📄 PAGINACIÓN
    paginator = Paginator(productos, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "Producto/lista2.html", {
        "page_obj": page_obj,
        "query": query,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "stock_invertido": stock_invertido,
        "ganancia": ganancia,
        "valor_venta_stock": valor_venta_stock,
    })
    

def exportar_excel_bodega2(productos):
    import openpyxl
    from django.http import HttpResponse

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventario Bodega 2"

    # Encabezados
    ws.append([
        'Código', 'Nombre', 'Categoría',
        'Ingreso', 'Salida', 'Stock',
        'Precio Compra', 'Precio Venta'
    ])

    # Datos
    for p in productos:
        stock = p.ingreso - p.salida

        ws.append([
            p.codigo,
            p.nombre,
            p.categoria,
            p.ingreso,
            p.salida,
            stock,
            float(p.compra),
            float(p.venta),
        ])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="inventario_bodega2.xlsx"'

    wb.save(response)
    return response



@login_required
def update(request, t):
    # print("ID:", t)

    producto = get_object_or_404(Producto, id=t)

    # print("Producto encontrado:", producto.nombre)

    if request.method == 'POST':
        form = UpdateProductoForm(request.POST, instance=producto)
        if form.is_valid():
            p = form.save(commit=False)

            # Campos adicionales
            nuevo_ing = form.cleaned_data.get('nuevo_ing')
            nuevo_compra = form.cleaned_data.get('nuevo_compra')
            nuevo_venta = form.cleaned_data.get('nuevo_venta')

            if nuevo_ing is not None:
                if nuevo_ing >= 0:
                    # Si es positivo, aumenta ingreso
                    p.ingreso += nuevo_ing
                else:
                    # Si es negativo, aumenta salida
                    p.salida += abs(nuevo_ing)

            if nuevo_compra is not None:
                p.compra = nuevo_compra

            if nuevo_venta is not None:
                p.venta = nuevo_venta

            p.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('ListaProd')
        else:
            messages.error(request, "Producto NO actualizado")
    else:
        form = UpdateProductoForm(instance=producto)

    return render(request, 'Producto/update.html', {
        'form': form,
        'producto': producto
    })


@login_required
def agotados2(request):

    productos = Producto2.objects.annotate(
        stock_calc=ExpressionWrapper(
            Coalesce(F('ingreso'), 0) - Coalesce(F('salida'), 0),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        ),
        valor_stock=ExpressionWrapper(
            (Coalesce(F('ingreso'), 0) - Coalesce(F('salida'), 0)) * Coalesce(F('compra'), 0),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        )
    ).filter(stock_calc__lte=0).order_by('codigo')

    paginator = Paginator(productos, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'Producto/agotados2.html', {
        'page_obj': page_obj
    })
    

@login_required
def update2(request, t):
   # print("ID:", t)

    producto = get_object_or_404(Producto2, id=t)

    #print("Producto encontrado:", producto.nombre)

    if request.method == 'POST':
        form = UpdateProductoForm(request.POST, instance=producto)
        if form.is_valid():
            p = form.save(commit=False)

            # Campos adicionales
            nuevo_ing = form.cleaned_data.get('nuevo_ing')
            nuevo_compra = form.cleaned_data.get('nuevo_compra')
            nuevo_venta = form.cleaned_data.get('nuevo_venta')

            if nuevo_ing is not None:
                if nuevo_ing >= 0:
                    # Si es positivo, aumenta ingreso
                    p.ingreso += nuevo_ing
                else:
                    # Si es negativo, aumenta salida
                    p.salida += abs(nuevo_ing)

            if nuevo_compra is not None:
                p.compra = nuevo_compra

            if nuevo_venta is not None:
                p.venta = nuevo_venta

            p.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('ListaProd2')
        else:
            messages.error(request, "Producto NO actualizado")
    else:
        form = UpdateProductoForm(instance=producto)

    return render(request, 'Producto/update.html', {
        'form': form,
        'producto': producto
    })




@login_required
def baja(request, t):
    producto = get_object_or_404(Producto, id=t)
    producto.estado = 0
    producto.save()
    messages.success(request, "Producto dado de baja correctamente.")
    return redirect('ListaProd')


@login_required
def alta(request, t):
    producto = get_object_or_404(Producto, id=t)
    producto.estado = 1
    producto.save()
    messages.success(request, "Producto dado de alta correctamente.")
    return redirect('ListaProd')


@login_required
def reporte_inversion(request):
    # 🔎 Buscador
    query = request.GET.get("q", "")
    productos = Producto.objects.all()

    if query:
        productos = productos.filter(
            Q(codigo__icontains=query) |
            Q(nombre__icontains=query) |
            Q(categoria__icontains=query)
        )

    # 📊 Calcular inversión por producto directamente en SQL
    productos = productos.annotate(
        inversion_total=ExpressionWrapper(
            (F("ingreso") - F("salida")) * F("compra"),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        )
    )

    # 📊 Calcular inversión global
    inversion_global = productos.aggregate(total=Sum("inversion_total"))["total"] or 0

    # 📄 Paginador (10 productos por página)
    paginator = Paginator(productos, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "Producto/reporte_inversion.html", {
        "page_obj": page_obj,
        "query": query,
        "inversion_global": inversion_global
    })
    
    



@login_required
def eliminar(request, t):
    producto = get_object_or_404(Producto, id=t)
    if request.method == "POST":
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f"Producto {nombre} eliminado definitivamente.")
        return redirect('ListaProd')
    return render(request, "Producto/eliminar.html", {"producto": producto})
    
    
    


@login_required
def eliminar2(request, t):
    producto = get_object_or_404(Producto, id=t)
    if request.method == "POST":
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f"Producto {nombre} eliminado definitivamente.")
        return redirect('ListaProd2')
    return render(request, "Producto/eliminar2.html", {"producto": producto})
    
    
