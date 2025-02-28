from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Contactos, WebUsuarios
from .serializers import ContactosSerializer, WebUsuariosListSerializer, WebUsuariosCreateUpdateSerializer
# Create your views here.


class ContactosViewSet(viewsets.ModelViewSet):  # Solo permite GET
    serializer_class = ContactosSerializer

    def get_queryset(self):
        return Contactos.objects.all() 
    
class WebUsuariosViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return WebUsuarios.objects.all()
    
    def get_serializer_class(self):
        # Devuelve un serializer diferente según la acción
        if self.action in ['list', 'retrieve']:
            return WebUsuariosListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return WebUsuariosCreateUpdateSerializer
        # Serializer por defecto si no coincide con ninguna acción específica
        return WebUsuariosListSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        with transaction.atomic():
            # Aquí puedes agregar lógica personalizada para la creación
            # Por ejemplo, crear primero el contacto y luego el usuario web
            self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            # Lógica personalizada para la actualización
            self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()

    
        
        

