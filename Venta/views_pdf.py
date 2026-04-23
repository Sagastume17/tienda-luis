from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from Venta.models import Venta
from django.contrib.auth.decorators import login_required

@login_required
def exportar_ventas_pdf(request):
    # Respuesta HTTP
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="ventas.pdf"'

    # Crear PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, "Reporte de Ventas")

    ventas = Venta.objects.all()
    y = 720
    for v in ventas:
        p.drawString(100, y, f"{v.fecha} - {v.nombre} - Q{v.total} - {v.usuario.username}")
        y -= 20
        if y < 50:  # salto de página
            p.showPage()
            p.setFont("Helvetica", 12)
            y = 750

    p.showPage()
    p.save()
    return response
