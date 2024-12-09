from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Organizacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True, default='correo_temporal@example.com')
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)
    organizacion = models.ForeignKey(
        Organizacion, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,  # Permitir que sea opcional en formularios
        default=None  # Usar None como valor por defecto
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Hotel(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)  # Cambié a CharField
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(default='correo_temporal@example.com')
    organizacion = models.ForeignKey(
        'Organizacion',
        on_delete=models.CASCADE,
        related_name='hoteles',
        default=None
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    ROLES = [
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('usuario', 'Usuario'),
    ]
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    hotel = models.ForeignKey(
        'Hotel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )
    organizacion = models.ForeignKey(
        'Organizacion',
        on_delete=models.CASCADE,
        related_name='usuarios',
        null=True,
        blank=True,
        default=None
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

class Habitacion(models.Model):
    TIPO_CHOICES = [
        ('estándar', 'Estándar'),
        ('suite', 'Suite'),
    ]
    
    numero = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)
    hotel = models.ForeignKey(
        'Hotel', 
        on_delete=models.CASCADE, 
        related_name='habitaciones'
    )
    habilitada = models.BooleanField(default=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tipo} - {self.numero} ({self.hotel.nombre})"

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('en uso', 'En Uso'),
        ('finalizada', 'Finalizada'),
    ]

    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='reservas')
    habitacion = models.ForeignKey('Habitacion', on_delete=models.CASCADE, related_name='reservas')
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='reservas')
    recepcionista = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas_asignadas')
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def save(self, *args, **kwargs):
        if self.fecha_entrada >= self.fecha_salida:
            raise ValueError("La fecha de entrada debe ser anterior a la fecha de salida.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.nombre}"

class Pago(models.Model):
    reserva = models.OneToOneField(
        'Reserva', 
        on_delete=models.CASCADE, 
        related_name='pago'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50, choices=[('tarjeta', 'Tarjeta'), ('efectivo', 'Efectivo')])

    def __str__(self):
        return f"Pago {self.reserva.id} - {self.monto}"
