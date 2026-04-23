from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nit', 'nombre', 'direccion', 'tel',]
        labels = {
            'nit': 'Nit del Proveedor',
            'nombre': 'Nombre del Proveedor',
            'direccion': 'Direccion de Proveedor',
            'tel': 'Telefono de Proveedor',
        }
        widgets = {
            'nit': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: 123456-7',
                'maxlength': '15',
                'autofocus':True,
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: Comercio',
                'maxlength': '1000'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: 2av. 1era calle',
                'maxlength': '1000'
            }),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: 1234-5678',
                'maxlength': '9'
            }),

        }





class UpdateProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nit', 'nombre', 'direccion', 'tel',]
        labels = {
            'nit': 'Nit del Proveedor',
            'nombre': 'Nombre del Proveedor',
            'direccion': 'Direccion de Proveedor',
            'tel': 'Telefono de Proveedor',
        }
        widgets = {
            'nit': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: 123456-7',
                'maxlength': '15',
                'autofocus':True,
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: Comercio',
                'maxlength': '1000'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: 2av. 1era calle',
                'maxlength': '1000'
            }),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: 1234-5678',
                'maxlength': '9'
            }),
        }


