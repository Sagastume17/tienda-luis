from django import forms
from .models import Producto

CATEGORIA = [
    ('Tienda', 'Tienda'),
    ('Ferreteria', 'Ferreteria'),
]


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'categoria', 'compra', 'venta', 'ingreso']
        labels = {
            'codigo': 'Código del Producto',
            'nombre': 'Nombre del Producto',
            'categoria': 'Categoría',
            'compra': 'Precio de Compra',
            'venta': 'Precio de Venta',
            'ingreso': 'Cantidad de Ingreso',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: PROD-001',
                'maxlength': '200',
                'autofocus':True,
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: Martillo de acero',
                'maxlength': '255'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }, choices=CATEGORIA),
            'compra': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'ingreso': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '0',
                'min': '0'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        compra = cleaned_data.get('compra')
        venta = cleaned_data.get('venta')

        if compra is not None and venta is not None and venta < compra:
            self.add_error('venta', 'El precio de venta debe ser mayor o igual al precio de compra.')

        ingreso = cleaned_data.get('ingreso')
        if ingreso is not None and ingreso < 0:
            self.add_error('ingreso', 'La cantidad de ingreso no puede ser negativa.')

        return cleaned_data



class UpdateProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'categoria', 'compra', 'venta', 'ingreso']
        labels = {
            'codigo': 'Código del Producto',
            'nombre': 'Nombre del Producto',
            'categoria': 'Categoría',
            'compra': 'Precio de Compra',
            'venta': 'Precio de Venta',
            'ingreso': 'Cantidad de Ingreso',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: PROD-001',
                'maxlength': '200',
                'autofocus':True,
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: Martillo de acero',
                'maxlength': '255'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }, choices=CATEGORIA),
            'compra': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'ingreso': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '0',
                'min': '0'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        compra = cleaned_data.get('compra')
        venta = cleaned_data.get('venta')

        if compra is not None and venta is not None and venta < compra:
            self.add_error('venta', 'El precio de venta debe ser mayor o igual al precio de compra.')

        ingreso = cleaned_data.get('ingreso')
        if ingreso is not None and ingreso < 0:
            self.add_error('ingreso', 'La cantidad de ingreso no puede ser negativa.')

        return cleaned_data

