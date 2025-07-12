from django import forms
from .models import Pedido

class ContactoForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    email = forms.EmailField(label='Correo electrónico')
    mensaje = forms.CharField(label='Mensaje', widget=forms.Textarea)
    
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre', 'direccion', 'correo', 'telefono', 'identificacion']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 2}),
        }