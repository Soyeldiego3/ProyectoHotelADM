from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'usuarioAPP/inicio.html')

def contacto(request):
    return render(request, 'usuarioAPP/contacto.html')