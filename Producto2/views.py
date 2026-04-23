from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Producto.models import Producto,Producto2
from user.models import User
from .form import ProductoForm, UpdateProductoForm
from django.core.paginator import Paginator
from django.db.models import Q, F, Sum, ExpressionWrapper, DecimalField


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


@login_required
def listado(request):
    # 🔎 Capturar búsqueda
    query = request.GET.get("q", "")
    productos = Producto.objects.all().order_by("id")

    if query:
        productos = productos.filter(
            Q(codigo__icontains=query) |
            Q(nombre__icontains=query) |
            Q(categoria__icontains=query)
        )

    # 📄 Paginador (25 productos por página)
    paginator = Paginator(productos, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "Producto/lista.html", {
        "page_obj": page_obj,
        "query": query,  # 👈 se pasa al template
    })
    

@login_required
def listado2(request):
    # 🔎 Capturar búsqueda
    query = request.GET.get("q", "")
    productos = Producto2.objects.all().order_by("codigo")

    if query:
        productos = productos.filter(
            Q(codigo__icontains=query) |
            Q(nombre__icontains=query) |
            Q(categoria__icontains=query)
        )

    # 📄 Paginador (25 productos por página)
    paginator = Paginator(productos, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "Producto/lista2.html", {
        "page_obj": page_obj,
        "query": query,  # 👈 se pasa al template
    })    



@login_required
def update(request, t):
    producto = get_object_or_404(Producto, id=t)
    form = UpdateProductoForm(instance=producto)
    if request.method == 'POST':
        form = UpdateProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('ListaProd')
        else:
            messages.error(request, "Producto NO actualizado")
            return redirect('ListaProd')

    return render(request, 'Producto/update.html', {'form': form})


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
