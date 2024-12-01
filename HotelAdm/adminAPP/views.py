from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm
from django.urls import reverse
# Create your views here.
def panel_clientes(request):
    context = {'usuario': 'Admin'}
    return render(request, 'adminAPP/paneles/panel-clientes.html',context)

def panel_hoteles(request):
    context = {'usuario': 'Admin'}
    return render(request, 'adminAPP/paneles/panel-hoteles.html', context)

def panel_usuarios(request):
    context = {'usuario': 'Admin'}
    return render(request, 'adminAPP/paneles/panel-usuarios.html', context)

def reservas(request):
    context = {'usuario': 'Usuario'}
    return render(request, 'adminAPP/reservas.html', context)

def reservasUsuario(request):
    context = {'usuario': 'Usuario'}
    return render(request, 'adminAPP/reservas_usuario.html', context)

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)  # No guarda aún
            cliente.activo = True  # Asigna el valor predeterminado
            cliente.save()
            return redirect('listar_cliente')  # Cambiar según tu URL
    else:
        form = ClienteForm()
    return render(request, 'adminAPP/crear_cliente.html', {'form': form})

def listar_clientes(request):
    query = request.GET.get('search', '')  # Obtén el parámetro de búsqueda
    clientes = Cliente.objects.all()
    
    if query:  # Si hay un término de búsqueda, filtra los clientes
        clientes = clientes.filter(nombre__icontains=query)  # Cambia "nombre" por el campo que quieras filtrar
    
    return render(request, 'adminAPP/listar_clientes.html', {'clientes': clientes, 'query': query})


def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        if 'guardar' in request.POST:
            form = ClienteForm(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
                url = reverse('listar_cliente')  # Verifica que esto no genere errores
                return redirect(url)
        elif 'eliminar' in request.POST:
            cliente.activo = False
            cliente.save()
            url = reverse('listar_cliente')  # Igual aquí
            return redirect(url)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'adminAPP/editar_cliente.html', {'form': form, 'cliente': cliente})