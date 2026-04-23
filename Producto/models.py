from django.db import models
from user.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver



class Producto(models.Model):
    codigo = models.CharField(max_length=200,unique=True,null=False,blank=False)
    nombre = models.CharField(max_length=1000,null=False,blank=False)
    categoria = models.CharField(max_length=400,null=True,blank=True)
    compra = models.DecimalField(max_digits=10,decimal_places=2,blank=False)
    venta = models.DecimalField(max_digits=10,decimal_places=2,blank=False)
    ingreso = models.IntegerField(blank=False,null=False,default=0)
    salida = models.IntegerField(blank=False,null=False,default=0)
    estado = models.BooleanField(blank=False,null=False,default=1)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)
    fecha = models.DateField(auto_now_add=True)

    class Meta:
       ordering = ["-codigo"]


    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    @property
    def stock_actual(self):
        return self.ingreso - self.salida
    
    
    @property
    def stock_actual(self):
        return self.ingreso - self.salida

    
    @stock_actual.setter
    def stock_actual(self, value):
        # Ajusta ingreso para reflejar el nuevo stock
        diferencia = value - (self.ingreso - self.salida)
        self.ingreso += diferencia

    
    
    @property
    def inversion_total(self):
        return (self.ingreso - self.salida) * self.compra

    
    @inversion_total.setter
    def inversion_total(self, value):
        if not self.compra or self.compra == 0:
        # No se puede calcular inversi贸n si el precio de compra es inv谩lido
            return  

        stock_deseado = value / self.compra
        diferencia = stock_deseado - (self.ingreso - self.salida)
        self.ingreso += diferencia




class Producto2(models.Model):
    codigo = models.CharField(max_length=200,unique=True,null=False,blank=False)
    nombre = models.CharField(max_length=1000,null=False,blank=False)
    categoria = models.CharField(max_length=400,null=True,blank=True)
    compra = models.DecimalField(max_digits=10,decimal_places=2,blank=False)
    venta = models.DecimalField(max_digits=10,decimal_places=2,blank=False)
    ingreso = models.IntegerField(blank=False,null=False,default=0)
    salida = models.IntegerField(blank=False,null=False,default=0)
    estado = models.BooleanField(blank=False,null=False,default=1)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)

    class Meta:
       ordering = ["-codigo"]


    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    @property
    def stock_actual(self):
        return self.ingreso - self.salida
    

class BitacoraPrecio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="bitacoras")
    precio_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    precio_nuevo = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Producto {self.producto.codigo} cambió de {self.precio_anterior} a {self.precio_nuevo}"


# Señal para registrar cambios de precio
@receiver(pre_save, sender=Producto)
def registrar_cambio_precio(sender, instance, **kwargs):
    if instance.pk:  # Solo si el producto ya existe
        try:
            producto_actual = Producto.objects.get(pk=instance.pk)
        except Producto.DoesNotExist:
            return

        # Si cambia el precio de venta
        if producto_actual.venta != instance.venta:
            BitacoraPrecio.objects.create(
                producto=instance,
                precio_anterior=producto_actual.venta,
                precio_nuevo=instance.venta,
                usuario=instance.usuario
            )

        # Si cambia el precio de compra
        if producto_actual.compra != instance.compra:
            BitacoraPrecio.objects.create(
                producto=instance,
                precio_anterior=producto_actual.compra,
                precio_nuevo=instance.compra,
                usuario=instance.usuario
            )
    