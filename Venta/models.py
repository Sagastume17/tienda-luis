from django.db import models
from user.models import User
from Producto.models import Producto,Producto2
import uuid
import datetime



class Venta(models.Model):
    factura = models.BigAutoField(primary_key=True)
    nit = models.CharField(max_length=15, blank=True, null=True, default='CF')
    nombre = models.CharField(max_length=250, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    tipo = models.CharField(
        max_length=50,
        choices=[('Proforma', 'Proforma'), ('FEL', 'FEL'), ('Cotizacion', 'Cotizacion')],
        blank=False,
        null=False
    )
    lugar = models.CharField(
        max_length=50,
        choices=[('Bodega 1', 'Bodega 1'), ('Bodega 2', 'Bodega 2')],
        blank=False,
        null=False,
        default='Bodega 1'
    )
    link = models.URLField(max_length=250, blank=True, null=True)
    numero = models.BigIntegerField(blank=True, null=True)
    serie = models.CharField(max_length=100, blank=True, null=True)
    anula = models.TextField(blank=True, null=True)
    fecha_fel = models.DateTimeField(blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, editable=False)
    fecha = models.DateField(blank=False,null=False)
    estado = models.IntegerField(choices=[(0, 'Pendiente'), (1, 'Procesada'), (2, 'Anulada')], default=0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ["factura"]

    def __str__(self):
        return f"Factura {self.factura} - {self.nombre} - Q.{self.total}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)  # protege historial
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    fecha_actualizo = models.DateTimeField(blank=True,null=True)
    
    class Meta:
        ordering = ["venta"]
        constraints = [
            models.UniqueConstraint(fields=['venta', 'producto'], name='unique_producto_por_venta')
        ]

    def __str__(self):
        return f"Detalle {self.venta.factura} - {self.producto.nombre}"

    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        
        



class DetalleVenta2(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto2, on_delete=models.PROTECT)  # protege historial
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    fecha_actualizo = models.DateTimeField(blank=True,null=True)
    
    class Meta:
        ordering = ["venta"]
        constraints = [
            models.UniqueConstraint(fields=['venta', 'producto'], name='unique_producto_por_venta_2')
        ]

    def __str__(self):
        return f"Detalle {self.venta.factura} - {self.producto.nombre}"

    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)        

