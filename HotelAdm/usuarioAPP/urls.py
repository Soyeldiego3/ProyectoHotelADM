from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.menuUsuarios, name='menuUsuarios'),
    path('', views.menuHoteles, name='menuHoteles'),
    path('/menuUsuarios', views.registroUsuarios, name='registroUsuario'),
    path('/menuHoteles', views.registroHoteles, name='registroHoteles'),
]