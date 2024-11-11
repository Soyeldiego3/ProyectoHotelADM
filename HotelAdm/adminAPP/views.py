from django.shortcuts import render

# Create your views here.
def panel_clientes(request):
    return render(request, 'adminAPP/paneles/panel-clientes.html')

def panel_hoteles(request):
    return render(request, 'adminAPP/paneles/panel-hoteles.html')

def panel_usuarios(request):
    return render(request, 'adminAPP/paneles/panel-usuarios.html')

def reservas(request):
    return render(request, 'adminAPP/reservas.html')

def reservasUsuario(request):
    return render(request, 'adminAPP/reservas_usuario.html')