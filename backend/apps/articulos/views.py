from rest_framework import viewsets
from .models import Articulos, Imagenes
from .serializers import ArticulosSerializer, ImagenesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import OuterRef, Subquery
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .filters import ArticuloFilter

class ArticulosViewSet(viewsets.ModelViewSet):
    serializer_class = ArticulosSerializer
    filter_backends = [DjangoFilterBackend]  # Habilitamos los filtros
    # filterset_class = ArticuloFilter  # Usamos el filtro personalizado
        
    def get_queryset(self):
        
        queryset = Articulos.objects.all()

        # Obtener los parámetros de la URL
        nrogru = self.request.query_params.get('nrogru', None)
        nrosub = self.request.query_params.get('nrosub', None)
        precio_min = self.request.query_params.get('precio_min', None)
        precio_max = self.request.query_params.get('precio_max', None)
        codigo = self.request.query_params.get('codigo', None)
        nombre = self.request.query_params.get('nombre', None)
        observ = self.request.query_params.get('observ', None)

        # Aplicar filtros si los parámetros están presentes
        if nrogru is not None:
            queryset = queryset.filter(nrogru=nrogru)
        if nrosub is not None:
            queryset = queryset.filter(nrosub=nrosub)
        if precio_min is not None:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max is not None:
            queryset = queryset.filter(precio__lte=precio_max)
        if codigo is not None:
            queryset = queryset.filter(codigo__icontains=codigo)
        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
        if observ is not None:
            queryset = queryset.filter(observ__icontains=observ)
        
        imagenes = Imagenes.objects.all()        

        imagenes_dict = {}
        for img in imagenes:
            
            if img.codimg not in imagenes_dict:
                imagenes_dict[img.codimg] = []
            imagenes_dict[img.codimg].append(img)
        # Agregar las imágenes a los artículos en memoria
        for q in queryset:
            q.imagenes_cache = imagenes_dict.get(q.codigo, [])  # Guardar imágenes en memoria
            
        return queryset


    
    # @method_decorator(cache_page(60 * 60 * 2))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    
    
    
    
    
class ImagenesViewSet(viewsets.ModelViewSet):
    queryset = Imagenes.objects.all()
    serializer_class = ImagenesSerializer



