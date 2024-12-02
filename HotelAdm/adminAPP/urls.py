from django.urls import path, include
from . import views


urlpatterns = [
    path('panel', views.panel_clientes, name='clientes'),
    path('usuarios', views.panel_usuarios, name='usuarios'),
    path('hoteles', views.panel_hoteles, name='hoteles'),
    path('clientes', views.panel_clientes, name='clientes'),

    path('reservas', views.reservas, name='reservas'),
    path('reservasUsuario', views.reservasUsuario, name='reservasUsuario'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    #path('listar_cliente/', views.listar_clientes, name='listar_cliente'),
    path('editar_cliente/<int:pk>/', views.editar_cliente, name='editar_cliente'),

    path('crear_hotel/', views.crear_hotel, name='crear_hotel'),
    path('editar_hotel/<int:pk>/', views.editar_hotel, name='editar_hotel'),
]