from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.menuUsuarios, name='menuUsuarios'),
    path('', views.menuHoteles, name='menuHoteles'),
    path('/menuUsuarios', views.registroUsuario, name='registroUsuario'),
    path('/menuHoteles', views.registroHoteles, name='registroHoteles'),
    
]