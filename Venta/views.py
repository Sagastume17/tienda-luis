from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Producto.models import Producto
from Cliente.models import Cliente
from Venta.models import Venta, DetalleVenta
from .form import VentaForm, DetalleVentaForm
from django.utils import timezone
from django.db.models import Q, Sum
from django.db import transaction
import uuid
from django.core.paginator import Paginator
from django.http import HttpResponse
from .reportes import Factura
from django.utils.dateparse import parse_date
from datetime import datetime


######################## FEL #########################
import emisor
import receptor
import InfileFel
###################### FIN FEL #######################


@login_required
def nueva(request):
    form = VentaForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        try:
            v = form.save(commit=False)
            v.usuario = request.user
            v.token = uuid.uuid4()

            # 🔥 AQUÍ EL CAMBIO IMPORTANTE
            if form.cleaned_data.get('fecha'):
                v.fecha = form.cleaned_data['fecha']
            else:
                v.fecha = timezone.now()

            v.save()

            if form.cleaned_data['lugar'] == 'Bodega 1':
                messages.success(request, f'Venta {v.factura} Iniciada!')
                return redirect('DetalleVenta', v.token)
            else:
                messages.success(request, f'Venta {v.factura} Iniciada!')
                return redirect('DetalleVenta2', v.token)

        except Exception as e:
            messages.error(request, f'Error al iniciar Venta: {str(e)}')
            return redirect('NuevaVenta')

    return render(request, 'Venta/nueva.html', {'form': form})



@login_required
def listado(request):
    # 🔎 Capturar parámetros de búsqueda
    query = request.GET.get("q", "")
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    ventas = Venta.objects.all().order_by("-factura")

    # Filtro por texto (nit y nombre)
    if query:
        ventas = ventas.filter(
            Q(nit__icontains=query) |
            Q(nombre__icontains=query)
        )

    # Filtro por rango de fechas
    if fecha_inicio and fecha_fin:
        ventas = ventas.filter(
            fecha__range=[parse_date(fecha_inicio), parse_date(fecha_fin)]
        )

    # 📄 Paginador (15 ventas por página)
    paginator = Paginator(ventas, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "Venta/lista.html", {
        "page_obj": page_obj,
        "query": query,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
    })




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum
from decimal import Decimal
from datetime import datetime



@login_required
def detalle(request, t):

    venta = get_object_or_404(Venta, token=t)
    form = DetalleVentaForm()
    detalles = DetalleVenta.objects.filter(venta=venta).order_by('id')

    cliente_existe = (
        Cliente.objects.filter(nit=str(venta.nit))
        .values('nit', 'nombre', 'direccion')
        .first()
        or {'nit': 'CF', 'nombre': 'Consumidor Final', 'direccion': 'Ciudad'}
    )

    if request.method == 'POST':

        # =====================================
        # 🔍 BUSCAR PRODUCTO (ESCÁNER / TEXTO)
        # =====================================
        if 'buscar' in request.POST:

            termino = request.POST.get('buscar')

            if not termino:
                messages.error(request, 'Campo vacío')
                return redirect('DetalleVenta', t)

            querys = Q(codigo=termino) | Q(nombre__icontains=termino)
            busqueda = Producto.objects.filter(querys)

            return render(request, 'Venta/detalle.html', {
                'v': venta,
                'form': form,
                'detalle': detalles,
                'c': cliente_existe,
                'q': True,
                'prod': busqueda
            })

        # =====================================
        # ➕ AGREGAR PRODUCTO
        # =====================================
        elif 'agregar' in request.POST:

            try:
                cantidad = int(request.POST.get('cantidad', 1))
            except:
                cantidad = 1

            codigo = request.POST.get('codigo')

            # 🔥 BUSCAR POR CÓDIGO (ESCÁNER)
            if codigo:
                p = Producto.objects.filter(codigo=codigo).first()
                if not p:
                    messages.error(request, "Producto no encontrado por código")
                    return redirect('DetalleVenta', t)

            # 🔥 BUSCAR POR ID (BOTÓN)
            else:
                try:
                    prod_id = int(request.POST.get('prod'))
                    p = Producto.objects.get(id=prod_id)
                except:
                    messages.error(request, "Producto no encontrado")
                    return redirect('DetalleVenta', t)

            # VALIDAR STOCK
            if cantidad > p.stock_actual:
                messages.error(request, f'Solo hay {p.stock_actual} en stock')
                return redirect('DetalleVenta', t)

            with transaction.atomic():

                dt = DetalleVenta.objects.filter(producto=p, venta=venta).first()

                if dt:
                    dt.cantidad += cantidad
                    dt.fecha_actualizo = datetime.today()
                    dt.save()
                else:
                    dt = form.save(commit=False)
                    dt.venta = venta
                    dt.producto = p
                    dt.precio_unitario = p.venta
                    dt.cantidad = cantidad
                    dt.fecha_actualizo = datetime.today()
                    dt.save()

                # 🔥 RECALCULAR TOTAL
                total = DetalleVenta.objects.filter(venta=venta).aggregate(
                    total=Sum('total')
                )['total'] or Decimal(0)

                venta.total = total
                venta.save()

                # 🔥 ACTUALIZAR INVENTARIO
                p.salida += cantidad
                p.save()

            return redirect('DetalleVenta', t)

        # =====================================
        # ❌ QUITAR PRODUCTO
        # =====================================
        elif 'quitar' in request.POST:

            try:
                dt = DetalleVenta.objects.get(
                    id=request.POST['cor_detalle'],
                    venta=venta
                )

                pr = dt.producto

                pr.salida = max(0, pr.salida - dt.cantidad)
                pr.save()

                dt.delete()

                total = DetalleVenta.objects.filter(venta=venta).aggregate(
                    total=Sum('total')
                )['total'] or Decimal(0)

                venta.total = total
                venta.save()

            except:
                messages.error(request, "Error al quitar producto")

            return redirect('DetalleVenta', t)

        # =====================================
        # 🗑 DESCARTAR VENTA
        # =====================================
        elif 'descartar' in request.POST:

            with transaction.atomic():

                for dt in DetalleVenta.objects.filter(venta=venta):
                    pr = dt.producto
                    pr.salida = max(0, pr.salida - dt.cantidad)
                    pr.save(update_fields=['salida'])

                DetalleVenta.objects.filter(venta=venta).delete()
                venta.delete()

            messages.warning(request, "Venta descartada")
            return redirect('NuevaVenta')

        # =====================================
        # ✅ FINALIZAR VENTA
        # =====================================
        elif 'terminar' in request.POST:

            venta.nit = request.POST.get('nit')
            venta.nombre = request.POST.get('nombre')
            venta.direccion = request.POST.get('direccion')

            # =====================================
            # 🔥 PROFORMA CON DESCUENTO
            # =====================================
            if venta.tipo == 'Proforma':

                descuento = request.POST.get('descuento', 0)

                try:
                    venta.descuento = Decimal(descuento)
                except:
                    venta.descuento = Decimal(0)

                total = DetalleVenta.objects.filter(venta=venta).aggregate(
                    total=Sum('total')
                )['total'] or Decimal(0)

                if venta.descuento > 0:
                    porcentaje = venta.descuento / Decimal(100)
                    total = total - (total * porcentaje)

                venta.total = total
                venta.save()

                messages.info(request, venta.factura)
                return redirect('NuevaVenta')

            # =====================================
            # 🔥 FEL
            # =====================================
            elif venta.tipo == 'FEL':

                venta.save()
                certificar_fel(request, venta.factura)

                return redirect('NuevaVenta')

            # =====================================
            # 🔥 NORMAL
            # =====================================
            else:

                venta.save()
                messages.success(request, "Venta finalizada")

                return redirect('NuevaVenta')

    return render(request, 'Venta/detalle.html', {
        'v': venta,
        'form': form,
        'detalle': detalles,
        'c': cliente_existe
    })


from decimal import Decimal
def certificar_fel(request,venta):
    # Obtener la venta
    datoscliente = Venta.objects.filter(factura=venta).first()
    if not datoscliente:
        messages.error(request, "No se encontró la venta.")
        return redirect('NuevaVenta')

    # Crear el DTE
    dte_fel_a_certificar = InfileFel.fel_dte()

    # Emisor
    emisor_fel = emisor.emisor()
    emisor_fel.set_direccion('Aldea Santa Rosalia', '19001', 'Zacapa', 'Zacapa', 'GT')
    emisor_fel.set_datos_emisor(
        'GEN', '1', 'correo@demo.com', '34390138',
        'JOSÉ LUIS, GUZMÁN ESTRADA', 'TIENDA Y LIBRERIA LA ECONOMICA'
    )

    # Receptor
    receptor_fel = receptor.receptor()
    receptor_fel.set_direccion(datoscliente.direccion, '19001', 'ZACAPA', 'ZACAPA', 'GT')
    receptor_fel.set_datos_receptor('correo@gmail.com', datoscliente.nit, datoscliente.nombre)

    # Datos generales
    dte_fel_a_certificar.set_clave_unica(f'{uuid.uuid4()}{venta}')
    dte_fel_a_certificar.set_datos_generales('GTQ', f'{datoscliente.fecha}T00:00:00-06:00', 'FACT')
    dte_fel_a_certificar.set_datos_emisor(emisor_fel)
    dte_fel_a_certificar.set_datos_receptor(receptor_fel)

    # Frases FEL
    dte_fel_a_certificar.frase_fel.set_frase('1', '1')

    # Totales
    total_fel = InfileFel.totales()
    totales_impuestos = InfileFel.total_impuesto()

    num = 0
    acutotal = 0
    acuiva = 0
    miventa = 0

    # Detalle de la venta
    for item in DetalleVenta.objects.filter(venta=venta):
        num += 1
        item_1 = InfileFel.item()
        item_1_impuesto = InfileFel.impuesto()

        # Datos del ítem
        item_1.set_numero_linea(num)
        item_1.set_bien_o_servicio('B')
        item_1.set_cantidad(item.cantidad)
        item_1.set_unidad_medida('UND')
        item_1.set_descripcion(item.producto.nombre)
        item_1.set_precio_unitario(item.precio_unitario)
        item_1.set_precio(item.cantidad * item.precio_unitario)
        item_1.set_descuento(0)
        item_1.set_total(item.total)

        # Cálculo de IVA (suponiendo precio con IVA incluido)
        grav = round((item.total / 112) * 100, 2)
        iva = round((grav * 12) / 100, 2)

        # Impuestos del ítem
        item_1_impuesto.set_monto_impuesto(iva)
        item_1_impuesto.set_monto_gravable(grav)
        item_1_impuesto.set_codigo_unidad_gravable(1)
        item_1_impuesto.set_nombre_corto('IVA')
        item_1.set_impuesto(item_1_impuesto)

        # Acumulados
        acutotal += grav
        acuiva += iva
        miventa += item.total

        # Agregar ítem al DTE
        dte_fel_a_certificar.agregar_item(item_1)

    # Totales generales
    #total_fel.set_gran_total(miventa)
    #totales_impuestos.set_nombre_corto('IVA')
    #totales_impuestos.set_total_monto_impuesto(acuiva)
    #total_fel.set_total_impuestos(totales_impuestos)
    #dte_fel_a_certificar.agregar_totales(total_fel)
    
    # =========================================
# DESCUENTO GENERAL
# =========================================

    descuento = datoscliente.descuento if datoscliente.descuento else Decimal(0)

    subtotal = miventa

    if descuento > 0:

        porcentaje = descuento / Decimal(100)

        descuento_monto = subtotal * porcentaje

        total_final = subtotal - descuento_monto

    # 🔥 RECALCULAR IVA
        gravable = round((total_final / 112) * 100, 2)
        iva_final = round((gravable * 12) / 100, 2)

    else:

        descuento_monto = Decimal(0)
        total_final = subtotal
        iva_final = acuiva

# =========================================
# TOTALES FEL
# =========================================

    total_fel.set_gran_total(round(total_final, 2))

    totales_impuestos.set_nombre_corto('IVA')

    totales_impuestos.set_total_monto_impuesto(round(iva_final, 2))

    total_fel.set_total_impuestos(totales_impuestos)

    dte_fel_a_certificar.agregar_totales(total_fel)

    # Adenda opcional
    fel_adenda = InfileFel.adenda()
    fel_adenda.nombre = "factura_ruta"
    fel_adenda.valor = "s"
    dte_fel_a_certificar.agregar_adenda(fel_adenda)

    # Certificación
    certificacion_fel = dte_fel_a_certificar.certificar()
    if certificacion_fel["resultado"]:
        messages.success(
            request,
            f"https://report.feel.com.gt/ingfacereport/ingfacereport_documento?uuid={certificacion_fel['uuid']}"
        )
        Venta.objects.filter(factura=venta).update(
            link=f"https://report.feel.com.gt/ingfacereport/ingfacereport_documento?uuid={certificacion_fel['uuid']}",
            numero=certificacion_fel['numero'],
            serie=certificacion_fel['serie'],
            anula=certificacion_fel['uuid'],
            fecha_fel=certificacion_fel['fecha'],
            estado = 1
        )
        
        return redirect('NuevaVenta')
    else:
        for error_fel in certificacion_fel.get("descripcion_errores", []):
            messages.error(request, f"{error_fel['fuente']}: {error_fel['mensaje_error']}")
        
        return redirect('NuevaVenta')



@login_required
def anularfel(request, t):
    # Validar usuario
    if not request.user.is_authenticated or not request.user.is_active:
        return redirect('/')

    # Obtener venta por token
    datoscliente = get_object_or_404(Venta, token=t)

    dte_fel_a_anular = InfileFel.fel_dte()

    # Llamado a la certificadora FEL
    certificacion_fel = dte_fel_a_anular.anular(
        str(datoscliente.fecha_fel),
        '34390138',  # ⚠️ este código deberías parametrizarlo/configurarlo
        str(datoscliente.fecha_fel),
        datoscliente.nit,
        datoscliente.anula,
        datoscliente.serie
    )

    if certificacion_fel.get("resultado"):
        # Actualizar estado de la venta
        Venta.objects.filter(token=t).update(
            fecha_fel=datoscliente.fecha_fel,
            estado=2
        )
        messages.success(request, f'Anulación FEL exitosa. UUID: {certificacion_fel["uuid"]}')
    else:
        # Mostrar errores al usuario
        descripcion = certificacion_fel.get("descripcion", "Error desconocido")
        messages.error(request, f'No pudo ser certificada: {descripcion}')

        for error_fel in certificacion_fel.get("descripcion_errores", []):
            messages.error(request, f'{error_fel["fuente"]}: {error_fel["mensaje_error"]}')

    # Si necesitas los detalles de la venta
    detalles = DetalleVenta.objects.filter(venta=datoscliente)

    return redirect('ListaVenta')
    
    
    
    
def ticket(request, f):
    if not request.user.is_authenticated and not request.user.is_active:
        return redirect('/')
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="detalle-compra-{f}.pdf"'
        r = Factura(f)
        response.write(r.run())
        return response