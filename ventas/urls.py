'''
Script con las urls asociadas a esta modulo

'''
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ventas import views

app_name = 'ventas'

urlpatterns = [
    path('', views.VentasBuscarView.as_view()),
    path('crear', views.VentasCrearView.as_view()),
    path('<int:pk>', views.VentasDetallesView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
