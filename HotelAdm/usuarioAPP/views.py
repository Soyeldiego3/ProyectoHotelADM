from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'usuarioAPP/homepage/inicio.html')

def cliente(request):
    return render(request, 'clienteAPP/homepage/inicio.html')