from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacto', views.contacto, name='contacto'),
    path('servicios', views.servicios, name='servicios'),
    path('login', views.login, name='login'),
    
    path('registroUsuarios', views.registroUsuarios, name='registroUsuarios'),
    path('registroHoteles', views.registroHoteles, name='registroHoteles'),
    path('menuUsuarios', views.menuUsuarios, name='menuUsuarios'),
    path('menuHoteles', views.menuHoteles, name='menuHoteles'),

]