from rest_framework import viewsets
from .models import Articulos
from .serializers import ArticulosSerializer

class ArticulosViewSet(viewsets.ModelViewSet):
    queryset = Articulos.objects.all()
    serializer_class = ArticulosSerializer


    def list(self, request, *args, **kwargs):
        print('http://localhost:8000/media/Imagenes/ART_001_1.jpg')
        return super().list(self, request, *args, **kwargs)
    
    
    



# print('http://localhost:8000/media/Imagenes/ART_001_1.jpg')
# URLDOMAIN+SETTINGS.MEDIA+ELEMENTO DE LA QUERY DEL INNERJOIN RIGHT ARTICULOS IMAGENES codeimg y codigo