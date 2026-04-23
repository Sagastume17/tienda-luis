from django.shortcuts import render
from django.db.models.functions import TruncMonth
from .models import Venta, DetalleVenta
from django.utils.timezone import now
from django.db.models import Sum, Count
import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date

# 📈 Tendencia de ventas por mes
@login_required
def reporte_tendencia(request):
    ventas = (
        Venta.objects.annotate(mes=TruncMonth("fecha"))
        .values("mes")
        .annotate(total_mes=Sum("total"))
        .order_by("mes")
    )
    return render(request, "Venta/reporte_general.html", {"ventas": ventas})

# 🏆 Top clientes
@login_required
def reporte_top_clientes(request):
    clientes = (
        Venta.objects.values("nombre")
        .annotate(total_compras=Sum("total"))
        .order_by("-total_compras")[:10]
    )
    return render(request, "Venta/reporte_por_cliente.html", {"clientes": clientes})

# 💰 Productos más rentables
@login_required
def reporte_productos_rentables(request):
    productos = (
        DetalleVenta.objects.values("producto__nombre")
        .annotate(total_ingresos=Sum("total"))
        .order_by("-total_ingresos")[:10]
    )
    return render(request, "Venta/reporte_productos.html", {"productos": productos})

# 👥 Comparación de ventas por usuario
@login_required
def reporte_por_usuario(request):
    usuarios = (
        Venta.objects.values("usuario__username")
        .annotate(total_vendido=Sum("total"))
        .order_by("-total_vendido")
    )
    return render(request, "Venta/reporte_por_usuario.html", {"usuarios": usuarios})


@login_required
def estadisticas_ventas(request):
    hoy = now()  # si tu campo fecha es DateField
    # Ventas procesadas del día
    ventas_dia = Venta.objects.filter(fecha=hoy, estado=1)
    ventas_dia2 = Venta.objects.filter(fecha=hoy, estado=1)

    # ✅ Ganancia global
    ganancias_global = ventas_dia.aggregate(total=Sum("total"))["total"] or 0

    # ✅ Ventas FEL
    fel_qs = ventas_dia.filter(tipo="FEL")  # case-insensitive
    fel_count = fel_qs.count()
    fel_total = fel_qs.aggregate(total=Sum("total"))["total"] or 0

    # ✅ Ventas Proforma
    proforma_qs = ventas_dia2.filter(tipo="Proforma")  # case-insensitive
    proforma_count = proforma_qs.count()
    proforma_total = proforma_qs.aggregate(total=Sum("total"))["total"] or 0

    context = {
        "ganancias_global": ganancias_global,
        "fel_count": fel_count,
        "fel_total": fel_total,
        "proforma_count": proforma_count,
        "proforma_total": proforma_total,
    }
    return render(request, "Venta/estadisticas.html", context)


@login_required
def exportar_ventas_excel(request):
    # Crear libro y hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Ventas"

    # Encabezados
    ws.append(["Fecha", "Cliente", "Total", "Usuario"])

    # Datos
    ventas = Venta.objects.all()
    for v in ventas:
        ws.append([v.fecha, v.nombre, v.total, v.usuario.username])

    # Respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="ventas.xlsx"'
    wb.save(response)
    return response



@login_required
def reporte_ventas(request):
    # 📅 Capturar fechas desde GET
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    ventas = Venta.objects.filter(estado=1)  # solo procesadas

    # Filtrar por rango de fechas
    if fecha_inicio and fecha_fin:
        ventas = ventas.filter(
            fecha__range=[parse_date(fecha_inicio), parse_date(fecha_fin)]
        )

    # 📊 Total vendido por tipo FEL
    total_fel = ventas.filter(tipo="FEL").aggregate(total=Sum("total"))["total"] or 0

    # 📊 Total global de ventas
    total_global = ventas.aggregate(total=Sum("total"))["total"] or 0

    return render(request, "Venta/reporte_venta.html", {
        "total_fel": total_fel,
        "total_global": total_global,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
    })
