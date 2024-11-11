from django.urls import path
from . import views

urlpatterns = [
    path('panel', views.panel_clientes, name='clientes'),
    path('usuarios', views.panel_usuarios, name='usuarios'),
    path('hoteles', views.panel_hoteles, name='hoteles'),
    path('clientes', views.panel_clientes, name='clientes'),

    path('reservas', views.reservas, name='reservas'),
    path('reservasUsuario', views.reservasUsuario, name='reservasUsuario'),
]