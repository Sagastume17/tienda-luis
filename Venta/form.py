from django import forms
from .models import Venta, DetalleVenta,DetalleVenta2


from django import forms
from .models import Venta

class VentaForm(forms.ModelForm):
    
    fecha = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Venta
        fields = [
            'nit', 'tipo', 'lugar', 'fecha'
        ]
        widgets = {
            'nit': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ej: 123456-7',
                'maxlength': '15',
                'autofocus': True,
            }),
            'tipo': forms.Select(attrs={
                'class': 'selectpicker form-control',
                'data-style': 'btn-outline-info',
                'placeholder': 'Tipo Venta',
                'required': True
            }),
            'lugar': forms.Select(attrs={
                'class': 'selectpicker form-control',
                'data-style': 'btn-outline-info',
                'placeholder': 'Bodega Venta',
                'required': True
            }),
        }

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['cantidad',]
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 1,'style': 'width:80px;'}),
        }



class DetalleVentaForm2(forms.ModelForm):
    class Meta:
        model = DetalleVenta2
        fields = ['cantidad',]
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 1,'style': 'width:80px;'}),
        }