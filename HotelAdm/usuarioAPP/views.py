from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'usuarioAPP/homepage/inicio.html')

def menuHoteles(request):
    return render (request,'clienteAPP/homepage/menuHoteles.html')

def menuUsuarios(request):
    return render (request,'clienteAPP/homepage/menuUsuarios.html')

def registroUsuario(request):
    return render(request, 'clienteAPP/homepage/registroUsuario.html')

def registroHoteles(request):
    return render (request,'clienteAPP/homepage/registroHoteles.html')

