from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'usuarioAPP/homepage/inicio.html')

def cliente(request):
    return render(request, 'clienteAPP/homepage/inicio.html')

def menuHoteles(request):
    return render (request,'clienteAPP/homepage/menuHoteles.html')

def menuUsuarios(request):
    return render (request,'clienteAPP/homepage/menuUsuarios.html')

def registroUsuarios(request):
    return render(request, 'clienteAPP/homepage/registroUsuarios.html')

def registroHoteles(request):
    return render (request,'clienteAPP/homepage/registroHoteles.html')

def cliente(request):
    return render(request, 'clienteAPP/homepage/inicio.html')

def contacto(request):
    return render(request, 'usuarioAPP/contacto.html')

def login(request):
    return render(request, 'usuarioAPP/login.html')