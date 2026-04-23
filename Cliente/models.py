from django.db import models
from user.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator, RegexValidator


class Cliente(models.Model):
    
    nit = models.CharField(max_length=12,blank=False,null=False,default='CF',unique=True)
    nombre = models.CharField(max_length=250,blank=False,null=False,default='Consumidor Final')
    direccion = models.CharField(max_length=250,blank=True,null=True,default='Ciudad')
    telefono = models.CharField(max_length=20,blank=True,null=True,default='0000-0000',validators=[RegexValidator(r'^\d{4}-\d{4}$', 'Formato: 0000-0000')])
    compra = models.IntegerField(blank=True,null=True,default=0,validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True,default=Decimal('0.00'),validators=[MinValueValidator(Decimal('0.00'))])
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)


    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.nombre} ({self.nit})"



class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='compras')
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.CharField(max_length=250)
    monto = models.DecimalField(max_digits=12, decimal_places=2)

    
    class Meta:
        ordering = ['-fecha']
        

    def __str__(self):
        return f"{self.descripcion} - {self.monto}"
