from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Cliente, Hotel, Usuario, Habitacion, Reserva, Organizacion


class RegistroUsuarioForm(forms.ModelForm):
    # Campos de contraseña
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"}),
    )
    confirm_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirmar contraseña"}),
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'rol', 'hotel', 'organizacion', 'telefono', 'direccion']

        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de usuario"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "Correo electrónico"}),
            'hotel': forms.Select(attrs={"class": "form-control"}),
            'rol': forms.Select(attrs={"class": "form-control"}),
            'telefono': forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono"}),
            'direccion': forms.TextInput(attrs={"class": "form-control", "placeholder": "Dirección"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;',
            })

        # Asegurarse de que solo se muestren los hoteles activos
        self.fields['hotel'].queryset = Hotel.objects.filter(activo=True)
        self.fields['hotel'].empty_label = "Seleccione un hotel"

        # Verificar si el hotel está en el queryset de opciones disponibles
        if self.instance and self.instance.hotel and self.instance.hotel not in self.fields['hotel'].queryset:
            self.fields['hotel'].queryset = self.fields['hotel'].queryset.filter(id=self.instance.hotel.id)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Validar que las contraseñas coincidan
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Asegurar que la contraseña esté correctamente hasheada
        user.password = make_password(self.cleaned_data["password"])

        if commit:
            user.save()

        # Asignar el rol (campo 'rol')
        user.rol = self.cleaned_data.get('rol')
        user.save()

        return user


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'hotel', 'is_active', 'rol']

        widgets = {
            'username': forms.TextInput(attrs={"placeholder": "Nombre de usuario"}),
            'email': forms.EmailInput(attrs={"placeholder": "Correo electrónico"}),
            'telefono': forms.TextInput(attrs={"placeholder": "Teléfono"}),
            'hotel': forms.Select(attrs={"placeholder": "Seleccione el hotel"}),
            'is_active': forms.Select(choices=[(True, "Activo"), (False, "Inactivo")]),
            'rol': forms.Select(attrs={"placeholder": "Rol de usuario"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Usuario actual
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;',
            })

        self.fields['hotel'].queryset = Hotel.objects.filter(activo=True)
        self.fields['hotel'].empty_label = "Seleccione un hotel"

        if self.user and not self.user.is_superuser:
            self.fields['rol'].choices = [choice for choice in Usuario.ROLES if choice[0] != 'superadmin']

    def clean_rol(self):
        rol = self.cleaned_data.get('rol')
        if self.user and self.user.rol == 'admin' and rol == 'superadmin':
            raise ValidationError("Un usuario con rol 'Admin' no puede ser asignado como 'SuperAdmin'.")
        return rol

class OrganizacionForm(forms.ModelForm):
    class Meta:
        model = Organizacion
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la organización'})
        }

class ClienteForm(forms.ModelForm):
    organizacion = forms.ModelChoiceField(
        queryset=Organizacion.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    telefono = forms.CharField(
        validators=[RegexValidator(r'^\+?\d{9,15}$', message="Introduzca un número de teléfono válido.")],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono"})
    )

    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'telefono', 'direccion', 'organizacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;',
            })


class HotelForm(forms.ModelForm):
    organizacion = forms.ModelChoiceField(
        queryset=Organizacion.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;'
        })
    )

    class Meta:
        model = Hotel
        fields = ['nombre', 'direccion', 'telefono', 'correo', 'organizacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;',
            })


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'habitacion', 'hotel', 'fecha_entrada', 'fecha_salida', 'recepcionista']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #1f2235; color: #f8f9fa; border: 1px solid #f8f9fa;',
            })

        if user:
            self.instance.recepcionista = user

    def clean(self):
        cleaned_data = super().clean()
        fecha_entrada = cleaned_data.get("fecha_entrada")
        fecha_salida = cleaned_data.get("fecha_salida")

        if fecha_entrada and fecha_salida and fecha_entrada >= fecha_salida:
            raise ValidationError("La fecha de entrada debe ser anterior a la fecha de salida.")

        return cleaned_data


class OrganizacionForm(forms.ModelForm):
    class Meta:
        model = Organizacion
        fields = ['nombre']
