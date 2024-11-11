from django.shortcuts import render

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