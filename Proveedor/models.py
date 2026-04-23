from django.db import models
from user.models import User

class Proveedor(models.Model):
    nit = models.CharField(max_length=15,unique=True,null=False,blank=False)
    nombre = models.CharField(max_length=1000,null=False,blank=False)
    direccion = models.CharField(max_length=1000,null=False,blank=False)
    tel = models.CharField(max_length=9,null=True,blank=True,default='')
    compras = models.IntegerField(blank=False,null=False,default=0)
    total = models.DecimalField(max_digits=12,decimal_places=2,blank=False,null=False,default=0.00)
    estado = models.BooleanField(blank=False,null=False,default=1)
    fecha = models.DateField(blank=True,null=True,auto_now_add=True)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)

    class Meta:
       ordering = ["-nit"]


    def __str__(self):
        return f"{self.nit} - {self.nombre}"