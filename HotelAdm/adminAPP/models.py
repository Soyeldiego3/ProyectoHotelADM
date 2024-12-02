from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True, default='correo_temporal@example.com')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Hotel(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(default='correo_temporal@example.com')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    # Campos adicionales
    nombre = models.CharField(max_length=100, default="temp_user")
    correo = models.EmailField(unique=True, default='correo@example.com')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    
    # Relación con el modelo Hotel
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campos adicionales
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    # Renombramos las relaciones de los campos 'groups' y 'user_permissions'
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='usuario_auth_groups',  # Cambia el nombre del reverse accessor
        related_query_name='usuario_auth_group',  # Cambia el nombre de la consulta
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='usuario_auth_permissions',  # Cambia el nombre del reverse accessor
        related_query_name='usuario_auth_permission',  # Cambia el nombre de la consulta
        blank=True
    )


class Habitacion(models.Model):
    numero = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50, choices=[('estándar', 'Estándar'), ('suite', 'Suite')])
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=0)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    habilitada = models.BooleanField(default=True)  # Indica si está operativa
    disponible = models.BooleanField(default=True)  # Indica si está ocupada o libre

    def __str__(self):
        return f"{self.tipo} - {self.numero} ({self.hotel.nombre})"

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('en uso', 'En Uso'),
        ('finalizada', 'Finalizada'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    recepcionista = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.nombre}"

class Pago(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50, choices=[('tarjeta', 'Tarjeta'), ('efectivo', 'Efectivo')])

    def __str__(self):
        return f"Pago {self.reserva.id} - {self.monto}"
