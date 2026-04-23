from . import views,view_reportes,views_bodega2,views_pdf
from django.urls import path


urlpatterns = [
    path('nueva-venta/',views.nueva,name="NuevaVenta"),
    path('detalle-venta/<uuid:t>',views.detalle,name="DetalleVenta"),
    path('lista-venta/',views.listado,name="ListaVenta"),
    path('ticket-venta/<int:f>',views.ticket,name="TicketVenta"),
    path('anular-venta/<uuid:t>',views.anularfel,name="AnulaFelVenta"),
    path('exportar-pdf-venta/',views_pdf.exportar_ventas_pdf,name="ExportarPDFVenta"),
    path('exportar-excel-venta/',view_reportes.exportar_ventas_excel,name="ExportarExcelVenta"),
    path('reporte-fel-venta/',view_reportes.reporte_ventas,name="ReporteFelVenta"),
    
    ## BODEGA 2 ##
    
    
    path('nueva-venta-2/',views_bodega2.nueva,name="NuevaVenta2"),
    path('detalle-venta-2/<uuid:t>',views_bodega2.detalle,name="DetalleVenta2"),
    path('lista-venta-2/',views_bodega2.listado,name="ListaVenta2"),
    path('ticket-venta-2/<int:t>',views_bodega2.ticket,name="TicketVenta2"),
    
    
    ## FIN BODEGA 2 ##
    
    
    #path('modificar-proveedor/<int:t>',views.update,name="UpdateProv"),
    #path('baja-proveedor/<int:t>',views.baja,name="BajaProv"),
    #path('alta-proveedor/<int:t>',views.alta,name="AltaProv"),
    
    path("reporte-general/", view_reportes.reporte_tendencia, name="reporte_general"),
    path("reporte-cliente/", view_reportes.reporte_top_clientes, name="reporte_cliente"),
    path("reporte-productos/", view_reportes.reporte_productos_rentables, name="reporte_productos"),
    path("reporte-usuario/", view_reportes.reporte_por_usuario, name="reporte_usuario"),
    path("reporte/estadisticas/", view_reportes.estadisticas_ventas, name="estadisticas_ventas"),
]


