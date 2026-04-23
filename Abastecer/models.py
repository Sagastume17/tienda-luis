from django.db import models
from user.models import User
from Proveedor.models import Proveedor
from Producto.models import Producto
from decimal import Decimal

class Abastecer(models.Model):
    factura = models.CharField(max_length=200,unique=True,null=False,blank=False)
    fecha_factura = models.DateField(blank=False,null=False)
    proveedor = models.CharField(max_length=15,null=False,blank=False)
    total = models.DecimalField(max_digits=12,decimal_places=2,blank=False,null=False,default=Decimal('0.00'))
    lugar = models.CharField(max_length=50,blank=False,null=False,default='Tienda')
    estado = models.BooleanField(blank=False,null=False,default=1)
    fecha = models.DateField(blank=False,null=False,auto_now_add=True)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)

    class Meta:
       ordering = ["-factura"]


    def __str__(self):
        return f"{self.factura} - {self.proveedor}"
    


class Detalle(models.Model):
    abastecedor = models.ForeignKey(Abastecer,on_delete=models.CASCADE,blank=False,null=False)
    prod = models.ForeignKey(Producto,on_delete=models.CASCADE,blank=False,null=False)
    compra_antes = models.DecimalField(max_digits=12,decimal_places=2,blank=False,null=False,default=Decimal('0.00'))    
    compra_ahora = models.DecimalField(max_digits=12,decimal_places=2,blank=False,null=False,default=Decimal('0.00'))
    venta_antes = models.DecimalField(max_digits=12,decimal_places=2,blank=False,null=False,default=Decimal('0.00'))
    venta_ahora = models.DecimalField(max_digits=12,decimal_places=2,blank=False,null=False,default=Decimal('0.00'))
    ingreso_antes = models.IntegerField(blank=False,null=False,default=0)
    ingreso_ahora = models.IntegerField(blank=False,null=False,default=0)
    estado = models.BooleanField(blank=False,null=False,default=True)
    fecha = models.DateField(blank=False,null=False,auto_now_add=True)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)

    class Meta: 
        ordering = ["-abastecedor__fecha_factura"]


    def __str__(self):
        return f"Detalle de factura {self.abastecedor.factura} - Producto {self.prod.nombre}"
    
    @property
    def total(self):
        return self.compra_ahora * self.ingreso_ahora

    
        