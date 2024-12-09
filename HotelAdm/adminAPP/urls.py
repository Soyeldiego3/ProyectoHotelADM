from django.urls import path
from . import views


urlpatterns = [
    path('panel', views.panel_clientes, name='clientes'),
    path('usuarios', views.panel_usuarios, name='usuarios'),
    path('hoteles', views.panel_hoteles, name='hoteles'),
    path('clientes', views.panel_clientes, name='clientes'),

    path('reservas', views.reservas, name='reservas'),
    path('reservasUsuario', views.reservasUsuario, name='reservasUsuario'),
    #path('crear_cliente', views.crear_cliente, name='crear_cliente'),
    #path('listar_cliente/', views.listar_clientes, name='listar_cliente'),
    path('editar_cliente/<int:pk>', views.editar_cliente, name='editar_cliente'),

    path('crear_hotel', views.crear_hotel, name='crear_hotel'),
    path('editar_hotel/<int:pk>/', views.editar_hotel, name='editar_hotel'),
    
    path('crear_usuario', views.crear_usuario, name='crear_usuario'),
    path('editar_usuario/<int:pk>', views.editar_usuario, name='editar_usuario'),

    path('crear_organizacion/', views.crear_organizacion, name='crear_organizacion'),
    path('editar_organizacion/<int:pk>/', views.editar_organizacion, name='editar_organizacion'),
    path('eliminar_organizacion/<int:pk>/', views.eliminar_organizacion, name='eliminar_organizacion'),
    path('organizaciones/', views.listar_organizaciones, name='listar_organizaciones'),


    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    
]