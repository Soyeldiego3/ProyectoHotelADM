from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'usuarioAPP/homepage/inicio.html')

def cliente(request):
    return render(request, 'clienteAPP/homepage/inicio.html')

def contacto(request):
    return render(request, 'usuarioAPP/contacto.html')

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
