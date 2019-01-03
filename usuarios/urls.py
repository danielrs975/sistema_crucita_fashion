"""
Este script contiene los urls relacionados
con esta aplicacion
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from usuarios import views

app_name = "inventario"

urlpatterns = [
    path('usuarios/crear', views.UsuarioCrearViewSuperUsuario.as_view(), name="crear"),
    path('usuarios/registrarse', views.UsuarioRegistroView.as_view(), name="registro")
]

urlpatterns = format_suffix_patterns(urlpatterns)
