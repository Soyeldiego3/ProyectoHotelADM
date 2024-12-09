from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente, Hotel, Usuario, Organizacion
from .forms import ClienteForm, HotelForm, RegistroUsuarioForm, ReservaForm, EditarUsuarioForm, OrganizacionForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth.forms import AuthenticationForm


# Decorador para roles

# Decorador para roles
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verifica si el usuario está autenticado
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Debes iniciar sesión para acceder a esta página.")
            
            # Verifica si el usuario tiene alguno de los roles permitidos
            user_role = request.user.rol  # Si usas un campo 'rol' en el modelo Usuario
            if user_role not in allowed_roles:
                return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

#@login_required
#@role_required(allowed_roles=['superadmin', 'admin'])
# Paneles
#def panel_clientes(request):
#    query = request.GET.get('search', '')
#    clientes = Cliente.objects.all()
#    if query:
#        clientes = clientes.filter(nombre__icontains=query)
#    return render(request, 'adminAPP/paneles/panel-clientes.html', {'clientes': clientes, 'query': query, 'usuario': request.user.username})

@login_required
@role_required(allowed_roles=['superadmin', 'admin'])
# Paneles
def panel_clientes(request):
    query = request.GET.get('search', '')
    usuario = request.user

    if usuario.rol == 'superadmin':
        clientes = Cliente.objects.all()
    else:
        clientes = Cliente.objects.filter(organizacion=usuario.organizacion)

    if query:
        clientes = clientes.filter(nombre__icontains=query)

    return render(request, 'adminAPP/paneles/panel-clientes.html', {
        'clientes': clientes,
        'query': query,
        'user': usuario,
    })

@login_required
@role_required(allowed_roles=['superadmin', 'admin'])
def panel_hoteles(request):
    query = request.GET.get('search', '')  # Obtén el término de búsqueda
    usuario = request.user

    # Filtrar hoteles según el rol del usuario
    if usuario.rol == 'superadmin':
        hoteles = Hotel.objects.all()  # Superadmin puede ver todos los hoteles
    else:
        if usuario.organizacion:
            # Filtrar por la organización asociada al usuario
            hoteles = Hotel.objects.filter(organizacion=usuario.organizacion)
        else:
            hoteles = Hotel.objects.none()  # Si el usuario no tiene hotel asignado, no mostrar

    # Aplicar búsqueda si hay un término
    if query:
        hoteles = hoteles.filter(nombre__icontains=query)

    return render(request, 'adminAPP/paneles/panel-hoteles.html', {
        'hoteles': hoteles,
        'query': query,
        'usuario': usuario.username,
    })

@login_required
@role_required(allowed_roles=['superadmin', 'admin'])

def panel_usuarios(request):
    query = request.GET.get('search', '')  # Obtener el término de búsqueda
    usuario = request.user

    # Filtrar usuarios según el rol y la organización del usuario autenticado
    if usuario.rol == 'superadmin':
        usuarios = Usuario.objects.all()  # Superadmin puede ver todos los usuarios
    else:
        # Filtrar por organización si el usuario tiene una organización asociada
        if usuario.organizacion:
            usuarios = Usuario.objects.filter(organizacion=usuario.organizacion)
        else:
            usuarios = Usuario.objects.none()  # Si no tiene organización asignada, no se muestran usuarios

        # Filtrar por hotel (comentado para posible uso futuro)
        # if usuario.hotel:
        #     usuarios = usuarios.filter(hotel_id=usuario.hotel)
        # else:
        #     usuarios = usuarios.none()  # Si no tiene hotel asignado, no se muestran usuarios

    # Aplicar búsqueda si hay un término
    if query:
        usuarios = usuarios.filter(username__icontains=query)

    return render(request, 'adminAPP/paneles/panel-usuarios.html', {
        'usuarios': usuarios,
        'query': query,
        'user': usuario,  # Pasar el usuario autenticado al contexto
    })


# Reservas
def reservas(request):
    return render(request, 'adminAPP/reservas.html', {'usuario': 'Usuario'})


def reservasUsuario(request):
    return render(request, 'adminAPP/reservas_usuario.html', {'usuario': 'Usuario'})

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST, user=request.user)  # Pasar el usuario autenticado
        if form.is_valid():
            form.save()
            return redirect('reservas')
    else:
        form = ReservaForm()
    return render(request, 'adminAPP/crear_reserva.html', {'form': form})

def crear_organizacion(request):
    if request.method == 'POST':
        form = OrganizacionForm(request.POST)
        if form.is_valid():
            organizacion = form.save()
            messages.success(request, "Organización creada exitosamente.")
            return redirect('crear_cliente', organizacion_id=organizacion.id)  # Redirige a la creación de cliente
    else:
        form = OrganizacionForm()

    return render(request, 'adminAPP/crear_organizacion.html', {'form': form})

# CRUD Cliente
def crear_cliente(request, organizacion_id=None):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.activo = True
            if organizacion_id:
                organizacion = Organizacion.objects.get(id=organizacion_id)
                cliente.organizacion = organizacion
            cliente.save()
            messages.success(request, "Cliente creado exitosamente.")
            return redirect('clientes')  # Redirige a la vista de clientes
        else:
            messages.error(request, "El formulario de cliente no es válido.")
    else:
        form = ClienteForm()

    return render(request, 'adminAPP/crear_cliente.html', {'form': form})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        if 'guardar' in request.POST:
            # Aquí estamos obteniendo el valor del checkbox y asegurándonos de que sea un booleano
            activo = True if request.POST.get('activo') == 'on' else False
            form = ClienteForm(request.POST, instance=cliente)
            if form.is_valid():
                # Asegurándonos de que el estado de 'activo' se guarda correctamente
                cliente.activo = activo
                form.save()
                url = reverse('clientes')  # Redirige a la lista de clientes después de guardar
                return redirect(url)
        elif 'eliminar' in request.POST:
            # Aquí desactivamos al cliente
            cliente.activo = False
            cliente.save()
            url = reverse('clientes')
            return redirect(url)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'adminAPP/editar_cliente.html', {'form': form, 'cliente': cliente})


# CRUD Hotel
def crear_hotel(request):
    if request.method == "POST":
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hoteles')  # Cambia 'hoteles' por la ruta que corresponda.
    else:
        form = HotelForm()
    organizaciones = Organizacion.objects.all()  # Obtener todas las organizaciones
    return render(request, 'adminAPP/crear_hotel.html', {'form': form, 'organizaciones': organizaciones})

def editar_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        if 'guardar' in request.POST:
            form = HotelForm(request.POST, instance=hotel)
            if form.is_valid():
                form.save()
                return redirect('hoteles')
        elif 'eliminar' in request.POST:
            hotel.activo = False
            hotel.save()
            return redirect('hoteles')
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'adminAPP/editar_hotel.html', {'form': form, 'hotel': hotel})


# CRUD Usuario

def crear_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('usuarios')  # Redirige al panel de usuarios
    else:
        form = RegistroUsuarioForm()
    return render(request, 'adminAPP/crear_usuario.html', {'form': form})

def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/admin/usuarios')  # Cambia esto por la URL a donde redirigir
    else:
        form = EditarUsuarioForm(instance=usuario, user=request.user)

    return render(request, 'adminAPP/editar_usuario.html', {'form': form})

# Inicio de sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirige al dashboard u otra página
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# Registro
def registro_view(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistroUsuarioForm()
    return render(request, "usuarioAPP/registro.html", {"form": form})


# Dashboard
@login_required
def dashboard_view(request):
    return render(request, 'adminAPP/dashboard.html')


# Listar organizaciones
def listar_organizaciones(request):
    search_query = request.GET.get('search', '')
    if search_query:
        organizaciones = Organizacion.objects.filter(nombre__icontains=search_query)
    else:
        organizaciones = Organizacion.objects.all()
    return render(request, 'adminAPP/listar_organizaciones.html', {'organizaciones': organizaciones})

# Crear una organización
def crear_organizacion(request):
    if request.method == 'POST':
        form = OrganizacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_organizaciones')
    else:
        form = OrganizacionForm()
    return render(request, 'adminAPP/crear_organizacion.html', {'form': form})

# Editar una organización
def editar_organizacion(request, pk):
    organizacion = get_object_or_404(Organizacion, pk=pk)
    if request.method == 'POST':
        form = OrganizacionForm(request.POST, instance=organizacion)
        if form.is_valid():
            form.save()
            return redirect('listar_organizaciones')
    else:
        form = OrganizacionForm(instance=organizacion)
    return render(request, 'adminAPP/crear_organizacion.html', {'form': form})

# Eliminar una organización
def eliminar_organizacion(request, pk):
    organizacion = get_object_or_404(Organizacion, pk=pk)
    organizacion.delete()
    return redirect('listar_organizaciones')