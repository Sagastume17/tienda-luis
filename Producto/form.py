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
                'maxlength': '255',
                'style': 'text-transform: uppercase;',
                'oninput': 'this.value = this.value.toUpperCase();'
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
    # Campo adicional para sumar nueva existencia
    nuevo_ing = forms.IntegerField(
        label="Nueva Existencia",
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0',
            'min': '0'
        })
    )
    # Campos adicionales para actualizar precios
    nuevo_compra = forms.DecimalField(
        label="Nuevo Precio Compra",
        required=False,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0'
        })
    )
    nuevo_venta = forms.DecimalField(
        label="Nuevo Precio Venta",
        required=False,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0'
        })
    )

    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'categoria', 'compra', 'venta', 'estado', 'usuario']
        labels = {
            'codigo': 'Código',
            'nombre': 'Nombre',
            'categoria': 'Categoría',
            'compra': 'Precio Compra',
            'venta': 'Precio Venta',
            'estado': 'Estado',
            'usuario': 'Usuario',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: Martillo de acero',
                'maxlength': '255',
                'style': 'text-transform: uppercase;',
                'oninput': 'this.value = this.value.toUpperCase();'
            }),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01','readonly':True}),
            'venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01','readonly':True}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }




