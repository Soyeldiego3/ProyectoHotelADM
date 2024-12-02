from django import forms
from adminAPP.models import Habitacion

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero', 'tipo', 'precio_por_noche', 'hotel', 'disponible']
