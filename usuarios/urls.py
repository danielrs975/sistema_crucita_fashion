"""
Este script contiene los urls relacionados
con esta aplicacion
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from usuarios import views

app_name = "inventario"

urlpatterns = [
    path('usuarios/crear', views.UsuarioCrearView.as_view(), name="crear"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
