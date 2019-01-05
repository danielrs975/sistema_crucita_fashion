"""
Script que contiene las pruebas
para las vistas de esta aplicacion
"""
from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status
from usuarios.models import Usuario, Group, GRUPOS
