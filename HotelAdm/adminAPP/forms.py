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
        
        # Asegurarse de que solo se muestren los hoteles activos
        self.fields['hotel'].queryset = Hotel.objects.filter(activo=True)
        self.fields['hotel'].empty_label = "Seleccione un hotel"
        
        # Verificar si el hotel está en el queryset de opciones disponibles
        if self.instance and self.instance.hotel and self.instance.hotel not in self.fields['hotel'].queryset:
            self.fields['hotel'].queryset = self.fields['hotel'].queryset.filter(id=self.instance.hotel.id)
        
        self.fields['direccion'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;'
        })

        self.fields['is_active'].widget = forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;'
        })


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'habitacion', 'hotel', 'fecha_entrada', 'fecha_salida']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;'
            })

        # Filtrar habitaciones disponibles
        if 'hotel' in self.data:
            try:
                hotel_id = int(self.data.get('hotel'))
                self.fields['habitacion'].queryset = Habitacion.objects.filter(hotel_id=hotel_id, disponible=True)
            except (ValueError, TypeError):
                pass  # Ignorar errores si no hay un hotel válido seleccionado
        elif self.instance.pk:
            self.fields['habitacion'].queryset = self.instance.hotel.habitacion_set.filter(disponible=True)