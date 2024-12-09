from django.contrib import admin
from adminAPP.models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista
    list_display = ('username', 'email', 'hotel', 'rol', 'fecha_creacion', 'activo')
    
    # Campos por los que se puede buscar
    search_fields = ('username', 'email')

    # Filtros que se pueden usar en la interfaz de administración
    list_filter = ('hotel', 'activo', 'rol')  # Agregado 'rol' para filtrar por el rol

    # Opciones de ordenación predeterminada (por ejemplo, por fecha de creación)
    ordering = ('fecha_creacion',)

    # Configuración para mostrar campos relacionados (como 'hotel') de manera más legible
    def hotel(self, obj):
        return obj.hotel.nombre if obj.hotel else "No asignado"
    hotel.admin_order_field = 'hotel'  # Permite ordenar por el hotel

    def rol(self, obj):
        return obj.get_rol_display()  # Mostrar el nombre del rol en lugar de la clave
    rol.admin_order_field = 'rol'  # Permite ordenar por el rol
