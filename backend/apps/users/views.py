from django.shortcuts import render
from rest_framework import viewsets
from .models import Contactos, WebUsuarios
from .serializers import ContactosSerializer, WebUsuariosSerializer
# Create your views here.


class ContactosViewSet(viewsets.ModelViewSet):  # Solo permite GET
    serializer_class = ContactosSerializer

    def get_queryset(self):
        return Contactos.objects.all() 
    
class WebUsuariosViewSet(viewsets.ModelViewSet):  # Solo permite GET
    serializer_class = WebUsuariosSerializer

    def get_queryset(self):
        return WebUsuarios.objects.all() 
    
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"DATA: {data}")
        
        

