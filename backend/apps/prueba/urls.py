# apps/prueba/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('prueba/', views.prueba_conexion, name='prueba-conexion'),
]
