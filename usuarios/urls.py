"""
Este script contiene los urls relacionados
con esta aplicacion
"""
# pylint: skip-file
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from usuarios import views

app_name = "usuarios"

urlpatterns = [
     path('usuarios/admin/crear', views.AdministracionCrearUsuariosView.as_view(), name="crear"),
     path('registro/', views.UsuarioRegistroView.as_view(), name="registro"),
     path('usuarios/admin/detalle/<int:pk>',
          views.AdministracionUsuariosView.as_view(), name="administracion"),
     path('login/', views.LoginView.as_view(), name="login"),
     path('usuarios/vendedor/detalles/<int:pk>', views.VendedorUsuarioView.as_view(),
          name="vendedor_detalles"),
     path('perfil/<int:pk>', views.PerfilView.as_view(), name="perfil"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
