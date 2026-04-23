# cliente/forms.py
from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nit', 'nombre', 'direccion', 'telefono',]
        widgets = {
            'nit': forms.TextInput(attrs={'class': 'form-control','placeholden':'Nit','autofocus':True,'required':True}),
            'nombre': forms.TextInput(attrs={'class': 'form-control','placeholden':'Nombre','required':True}),
            'direccion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

