from django.db import models
from user.models import User



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

    class Meta:
       ordering = ["nombre"]


    def __str__(self):
        return f"{self.nombre}"
    
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
        # No se puede calcular inversión si el precio de compra es inválido
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