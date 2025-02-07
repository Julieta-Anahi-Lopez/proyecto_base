from rest_framework import viewsets
from .models import Articulos, Imagenes
from .serializers import ArticulosSerializer, ImagenesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import OuterRef, Subquery
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ArticulosViewSet(viewsets.ModelViewSet):
    serializer_class = ArticulosSerializer
        
    def get_queryset(self):
        # Obtener todos los artículos
        articulos = Articulos.objects.all()

        # Obtener todas las imágenes en una sola consulta
        imagenes = Imagenes.objects.all()

        # Crear un diccionario con las imágenes organizadas por codimg
        imagenes_dict = {}
        for img in imagenes:
            if img.codimg not in imagenes_dict:
                imagenes_dict[img.codimg] = []
            imagenes_dict[img.codimg].append(img)

        # Agregar las imágenes a los artículos en memoria
        for articulo in articulos:
            articulo.imagenes_cache = imagenes_dict.get(articulo.codigo, [])  # Guardar imágenes en memoria

        return articulos
    
    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    
    
    
    
    
class ImagenesViewSet(viewsets.ModelViewSet):
    queryset = Imagenes.objects.all()
    serializer_class = ImagenesSerializer



