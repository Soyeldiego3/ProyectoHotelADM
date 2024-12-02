from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente, Hotel, Usuario
from .forms import ClienteForm, HotelForm, UsuarioForm
from django.urls import reverse
# Create your views here.
def panel_clientes(request):
    #context = {'usuario': 'Admin'}
    query = request.GET.get('search', '')  # Obtén el parámetro de búsqueda
    clientes = Cliente.objects.all()
    
    if query:  # Si hay un término de búsqueda, filtra los clientes
        clientes = clientes.filter(nombre__icontains=query)  # Cambia "nombre" por el campo que quieras filtrar
    
    return render(request, 'adminAPP/paneles/panel-clientes.html', {'clientes': clientes, 'query': query, 'usuario': 'Admin'})

def panel_hoteles(request):
    
    query = request.GET.get('search', '')  # Obtén el parámetro de búsqueda
    hoteles = Hotel.objects.all()
    
    if query:  # Si hay un término de búsqueda, filtra los clientes
        hoteles = hoteles.filter(nombre__icontains=query)  # Cambia "nombre" por el campo que quieras filtrar
    
    return render(request, 'adminAPP/paneles/panel-hoteles.html', {'hoteles': hoteles, 'query': query, 'usuario': 'Admin'})

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
            return redirect('clientes')  # Cambiar según tu URL
    else:
        form = ClienteForm()
    return render(request, 'adminAPP/crear_cliente.html', {'form': form})

#def listar_clientes(request):
#    query = request.GET.get('search', '')  # Obtén el parámetro de búsqueda
#   clientes = Cliente.objects.all()
    
#    if query:  # Si hay un término de búsqueda, filtra los clientes
#        clientes = clientes.filter(nombre__icontains=query)  # Cambia "nombre" por el campo que quieras filtrar
#    
#   return render(request, 'adminAPP/listar_clientes.html', {'clientes': clientes, 'query': query})


def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        if 'guardar' in request.POST:
            form = ClienteForm(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
                url = reverse('clientes')  # Verifica que esto no genere errores
                return redirect(url)
        elif 'eliminar' in request.POST:
            cliente.activo = False
            cliente.save()
            url = reverse('clientes')  # Igual aquí
            return redirect(url)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'adminAPP/editar_cliente.html', {'form': form, 'cliente': cliente})

def crear_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)  # Guarda un objeto Hotel
            hotel.save()
            return redirect('hoteles')  # Asegúrate de que 'hoteles' esté configurado en tus URLs
    else:
        form = HotelForm()
    return render(request, 'adminAPP/crear_hotel.html', {'form': form})


def editar_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        if 'guardar' in request.POST:
            form = HotelForm(request.POST, instance=hotel)
            if form.is_valid():
                form.save()
                url = reverse('hoteles')  # Verifica que esto no genere errores
                return redirect(url)
        elif 'eliminar' in request.POST:
            hotel.activo = False
            hotel.save()
            url = reverse('hoteles')  # Igual aquí
            return redirect(url)
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'adminAPP/editar_hotel.html', {'form': form, 'hotel': hotel})

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'adminAPP/crear_usuario.html', {'form': form})

def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        if 'guardar' in request.POST:
            form = UsuarioForm(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('usuarios')
        elif 'eliminar' in request.POST:
            usuario.activo = False
            usuario.save()
            return redirect('usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'adminAPP/editar_usuario.html', {'form': form, 'usuario': usuario})

