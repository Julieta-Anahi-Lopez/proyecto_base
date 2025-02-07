from rest_framework import viewsets
from .models import Articulos, Imagenes
from .serializers import ArticulosSerializer, ImagenesSerializer
from django.db.models import OuterRef, Subquery
from django.conf import settings

class ArticulosViewSet(viewsets.ModelViewSet):
    queryset = Articulos.objects.all()
    serializer_class = ArticulosSerializer
    print(settings.MEDIA_ROOT)
    
    


    # def list(self, request, *args, **kwargs):
    #     queryset = Articulos.objects.annotate(
    #     imagen=Subquery(
    #             Imagen.objects.filter(codeimg=OuterRef('codigo')).values('ruta')[:1]
    #         )
    #     )
    #     print('http://localhost:8000/media/Imagenes/ART_001_1.jpg')
    #     return super().list(self, request, *args, **kwargs)
    
    
class ImagenesViewSet(viewsets.ModelViewSet):
    queryset = Imagenes.objects.all()
    serializer_class = ImagenesSerializer



# print('http://localhost:8000/media/Imagenes/ART_001_1.jpg')
# URLDOMAIN+SETTINGS.MEDIA+ELEMENTO DE LA QUERY DEL INNERJOIN RIGHT ARTICULOS IMAGENES codeimg y codigo