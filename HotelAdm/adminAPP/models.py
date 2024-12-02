from django.db import models
from django.contrib.auth.models import AbstractUser

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    rol = models.CharField(
        max_length=50,
        choices=[('administrador', 'Administrador'), ('recepcionista', 'Recepcionista')]
    )
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, null=True, blank=True)

    # Agregar `related_name` para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_groups',  # Nombre único
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions',  # Nombre único
        blank=True,
        help_text='Permisos específicos para este usuario.'
    )

class Hotel(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre

class Habitacion(models.Model):
    numero = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50, choices=[('estándar', 'Estándar'), ('suite', 'Suite')])
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
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
