from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'telefono', 'activo')
    search_fields = ('nombre', 'correo')
    list_filter = ('activo',)