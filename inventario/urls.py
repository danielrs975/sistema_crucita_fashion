'''
Script que contiene los urls asociados
con este modulo
'''
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from inventario import views

app_name = "inventario"

urlpatterns = [
    path('productos/', views.ProductoBuscarView.as_view(), name='buscar'),
    path('productos/<int:pk>', views.ProductoDetallesView.as_view(), name='editar'),
    path('productos/crear', views.ProductoCrearView.as_view(), name='crear'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
