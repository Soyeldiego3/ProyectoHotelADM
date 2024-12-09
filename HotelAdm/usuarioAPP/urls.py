from django.urls import path, re_path
from . import views

from adminAPP.views import registro_view, dashboard_view
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('contacto', views.contacto, name='contacto'),
    path('servicios', views.servicios, name='servicios'),
    #path('login', views.login, name='login'),

    
    path('registroUsuarios', views.registroUsuarios, name='registroUsuarios'),
    path('registroHoteles', views.registroHoteles, name='registroHoteles'),
    path('menuUsuarios', views.menuUsuarios, name='menuUsuarios'),
    path('menuHoteles', views.menuHoteles, name='menuHoteles'),

    path('habitaciones', views.listar_habitaciones, name='listar_habitaciones'),
    path('habitaciones/crear', views.crear_habitacion, name='crear_habitacion'),
    path('habitaciones/editar/<int:pk>', views.editar_habitacion, name='editar_habitacion'),
    path('eliminar_habitacion/<int:pk>', views.eliminar_habitacion, name='eliminar_habitacion'),
    path('deshabilitar_habitacion/<int:pk>/', views.deshabilitar_habitacion, name='deshabilitar_habitacion'),
    path('habitaciones/cambiar_estado<int:habitacion_id>/', views.cambiar_estado_habitacion, name='cambiar_estado_habitacion'),
    path('habitaciones/', views.listar_habitaciones, name='listar_habitaciones'),
    path('habitaciones/cambiar_estado/<int:habitacion_id>', views.cambiar_estado_habitacion, name='cambiar_estado_habitacion'),
    path('habitaciones/cambiar_disponibilidad/<int:habitacion_id>', views.cambiar_disponibilidad_habitacion, name='cambiar_disponibilidad_habitacion'),

    path('dashboard/', dashboard_view, name="dashboard"),
    path('login/', auth_views.LoginView.as_view(template_name='usuarioAPP/login.html'), name='login'),
    path("registro", registro_view, name="registro"),
    path('logout/', LogoutView.as_view(), name='logout'),
]