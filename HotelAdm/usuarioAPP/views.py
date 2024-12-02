from django.shortcuts import render, redirect, get_object_or_404
from adminAPP.models import Habitacion, Hotel
from .forms import HabitacionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
def index(request):
    return render(request, 'usuarioAPP/homepage/inicio.html')

def cliente(request):
    return render(request, 'clienteAPP/homepage/inicio.html')

def contacto(request):
    return render(request, 'usuarioAPP/contacto.html')

def servicios(request):
    return render(request, 'usuarioAPP/servicios.html')

def login(request):
    return render(request, 'usuarioAPP/login.html')

# hoteles y usuario
def menuHoteles(request):
    context = {'usuario' : 'Usuario'}
    return render (request,'clienteAPP/menuHoteles.html', context)

def menuUsuarios(request):
    context = {'usuario' : 'Usuario'}
    return render (request,'clienteAPP/menuUsuarios.html', context)

def registroUsuarios(request):
    context = {'usuario' : 'Usuario'}
    return render(request, 'clienteAPP/homepage/registroUsuarios.html', context)

def registroHoteles(request):
    context = {'usuario' : 'Usuario'}
    return render (request,'clienteAPP/homepage/registroHoteles.html', context)



def listar_habitaciones(request):
    mostrar_habilitadas = request.GET.get('habilitadas', '1') == '1'
    habitaciones = Habitacion.objects.filter(habilitada=mostrar_habilitadas)

    hoteles = Hotel.objects.all()
    selected_hotel = request.GET.get('hotel')
    busqueda = request.GET.get('q', '')

    if selected_hotel:
        habitaciones = habitaciones.filter(hotel_id=selected_hotel)
    if busqueda:
        habitaciones = habitaciones.filter(numero__icontains=busqueda)

    return render(request, 'adminAPP/Habitacion_reservas/listar_habitaciones.html', {
        'habitaciones': habitaciones,
        'hoteles': hoteles,
        'selected_hotel': selected_hotel,
        'busqueda': busqueda,
        'mostrar_habilitadas': mostrar_habilitadas,
    })
def cambiar_estado_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    habitacion.habilitada = not habitacion.habilitada  # Cambiar el estado
    habitacion.save()
    return redirect('listar_habitaciones')
def crear_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_habitaciones')
    else:
        form = HabitacionForm()

    hoteles = Hotel.objects.all()
    return render(request, 'adminAPP/Habitacion_reservas/crear_habitacion.html', {'form': form, 'hoteles': hoteles})

def editar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('listar_habitaciones')
    else:
        form = HabitacionForm(instance=habitacion)

    hoteles = Hotel.objects.all()
    return render(request, 'adminAPP/Habitacion_reservas/editar_habitacion.html', {'form': form, 'hoteles': hoteles})

def eliminar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    habitacion.habilitada = False
    habitacion.save()
    return redirect('listar_habitaciones')

def deshabilitar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    habitacion.habilitada = False  # Cambia a deshabilitada
    habitacion.save()
    return redirect('listar_habitaciones')

def cambiar_estado_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    habitacion.habilitada = not habitacion.habilitada  # Cambiar estado habilitada
    habitacion.save()
    return redirect('listar_habitaciones')

def cambiar_disponibilidad_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    habitacion.disponible = not habitacion.disponible  # Cambiar estado disponible
    habitacion.save()
    return redirect('listar_habitaciones')