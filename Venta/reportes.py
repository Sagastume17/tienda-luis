from decimal import Decimal
from io import BytesIO
from reportlab.lib.styles import ParagraphStyle, TA_LEFT
from reportlab.lib.units import inch, mm, cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Image
from .models import Venta, DetalleVenta
from django.db.models import Sum


class Factura:
    def __init__(self, f):
        self.buf = BytesIO()
        self.factura = f

    def run(self):
        self.doc = SimpleDocTemplate(
            self.buf,
            title=f"Detalle-{self.factura}",
            pagesize=(78 * mm, 250 * mm),
            topMargin=5 * mm,
            bottomMargin=10 * mm
        )
        self.story = []
        self.encabezado()
        self.crearTabla()
        self.doc.build(self.story, onFirstPage=self.numeroPagina)
        pdf = self.buf.getvalue()
        self.buf.close()
        return pdf

    def encabezado(self):
        venta = Venta.objects.filter(factura=self.factura).first()
        if not venta:
            return

        fecha = venta.fecha.strftime('%d-%m-%Y') if venta.fecha else ""

        # LOGO
        try:
            imagen_logo = Image("Venta/images.jpg", width=150, height=75)
            self.story.append(imagen_logo)
        except:
            pass

        self.story.append(Spacer(1, 0.1 * inch))

        encabezado = [
            [Paragraph(f"<b>Factura No:</b> {self.factura}", self.estiloPC()),
             Paragraph(f"<b>Fecha:</b> {fecha}", self.estiloPC())],
            [Paragraph(f"<b>Cliente:</b> {venta.nombre}", self.estiloPC2())],
            [Paragraph(f"<b>NIT:</b> {venta.nit}", self.estiloPC2())],
            [Paragraph(f"<b>Dirección:</b> {venta.direccion}", self.estiloPC2())],
        ]

        table = Table(encabezado, colWidths=[3.5 * cm, 3.5 * cm])
        table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('SPAN', (0, 1), (-1, 1)),
        ]))

        self.story.append(table)
        self.story.append(Spacer(1, 0.1 * inch))

    def crearTabla(self):
        venta = Venta.objects.filter(factura=self.factura).first()
        detalles = DetalleVenta.objects.filter(venta=self.factura)

        data = [["Descripción", "Cantidad", "Total"]]

        for x in detalles:
            data.append([
                Paragraph(x.producto.nombre, self.estiloTexto()),
                x.cantidad,
                f"Q.{x.total:.2f}"
            ])

        # 🔥 CALCULOS CORRECTOS
        subtotal = detalles.aggregate(Sum('total'))['total__sum'] or Decimal(0)
        total_piezas = detalles.aggregate(Sum('cantidad'))['cantidad__sum'] or 0

        descuento = venta.descuento or Decimal(0)
        porcentaje = descuento / Decimal(100)
        descuento_monto = subtotal * porcentaje
        total_final = subtotal - descuento_monto

        # 🔥 MOSTRAR EN PDF
        data.append([
            Paragraph("<b>Subtotal:</b>", self.estiloTexto()),
            f"{total_piezas} piezas",
            f"Q.{subtotal:.2f}"
        ])

        if descuento > 0:
            data.append([
                Paragraph(f"<b>Descuento ({descuento}%):</b>", self.estiloTexto()),
                "",
                f"-Q.{descuento_monto:.2f}"
            ])

        data.append([
            Paragraph("<b>Total Final:</b>", self.estiloTexto()),
            "",
            f"Q.{total_final:.2f}"
        ])

        table = Table(data, colWidths=[4 * cm, 1.5 * cm, 2 * cm], hAlign='CENTER')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        self.story.append(table)

    def estiloPC(self):
        return ParagraphStyle(name='izq', fontName="Helvetica-Bold", fontSize=8, alignment=TA_LEFT)

    def estiloPC2(self):
        return ParagraphStyle(name='izq2', fontName="Helvetica", fontSize=8, alignment=TA_LEFT)

    def estiloTexto(self):
        return ParagraphStyle(name='txt', fontName='Helvetica', fontSize=8, alignment=TA_LEFT)

    def numeroPagina(self, canvas, doc):
        canvas.drawRightString(70 * mm, 10 * mm, f"Página {canvas.getPageNumber()}")