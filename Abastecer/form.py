from django import forms
from .models import Abastecer,Detalle

CATEGORIA = [
    ('Tienda', 'Tienda'),
    ('Ferreteria', 'Ferreteria'),
]


class AbastecerForm(forms.ModelForm):
    class Meta:
        model = Abastecer
        fields = ['factura', 'fecha_factura','proveedor', 'total', 'lugar',]
        labels = {
            'factura': 'Factura de Compra',
            'fecha_factura':'Fecha de Compra',
            'nombre': 'Nombre del Producto',
            'categoria': 'Categoría',
            'compra': 'Precio de Compra',
            'venta': 'Precio de Venta',
            'ingreso': 'Cantidad de Ingreso',
        }
        widgets = {
            'factura': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: 1234567890',
                'maxlength': '200',
                'autofocus':True,

            }),
            'fecha_factura': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'type':'date',
            }),
            'proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: 123456-7',
                'maxlength': '15',
            }),
            'total': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
            'lugar': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }, choices=CATEGORIA),
        }

    def clean(self):
        cleaned_data = super().clean()
        factura = cleaned_data.get('factura')
        total = cleaned_data.get('total')

        if total is not None and total < 0.00:
            self.add_error('total', 'El precio de la factura debe ser mayor a cero.')
        
        if factura and Abastecer.objects.filter(factura=factura).exists():
            self.add_error('factura', 'Ya existe un abastecimiento registrado con esta factura.')


        return cleaned_data



class UpdateAbastecerForm(forms.ModelForm):
    class Meta:
        model = Abastecer
        fields = ['factura', 'fecha_factura','proveedor', 'total', 'lugar',]
        labels = {
            'factura': 'Factura de Compra',
            'fecha_factura':'Fecha de Compra',
            'nombre': 'Nombre del Producto',
            'categoria': 'Categoría',
            'compra': 'Precio de Compra',
            'venta': 'Precio de Venta',
            'ingreso': 'Cantidad de Ingreso',
        }
        widgets = {
            'factura': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: 1234567890',
                'maxlength': '200',
                'autofocus':True,
            }),
            'fecha_factura': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'type':'date',
            }),
            'proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: 123456-7',
                'maxlength': '15'
            }),
            'total': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'lugar': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }, choices=CATEGORIA),
        }

    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get('total')

        if total is not None and total < 0.00:
            self.add_error('total', 'El precio de la factura debe ser mayor a cero.')


        return cleaned_data
    
    

class DetalleForm(forms.ModelForm):
    class Meta:
        model = Detalle
        fields = ['venta_ahora','compra_ahora','ingreso_ahora',]
        labels = {
            'venta_ahora': 'Factura de Compra',
            'compra_ahora':'Fecha de Compra',
            'ingreso_ahora': 'Nombre del Producto',
        }
        widgets = {
            'venta_ahora': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'compra_ahora': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'ingreso_ahora': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get('total')

        if total is not None and total < 0.00:
            self.add_error('total', 'El precio de la factura debe ser mayor a cero.')


        return cleaned_data    

