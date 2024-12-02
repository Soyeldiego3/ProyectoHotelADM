from django import forms
from .models import Cliente, Hotel, Usuario, Habitacion, Reserva

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'telefono', 'direccion']
        
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;'
            })


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['nombre', 'direccion', 'telefono', 'correo']
        
    def __init__(self, *args, **kwargs):
        super(HotelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;'
            })

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'correo', 'telefono', 'direccion', 'hotel', 'is_active']

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;'
            })
        self.fields['hotel'].queryset = Hotel.objects.filter(activo=True)
        self.fields['hotel'].empty_label = "Seleccione un hotel"