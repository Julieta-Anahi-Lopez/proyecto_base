from rest_framework import viewsets
from .models import Articulos
from .serializers import ArticulosSerializer

class ArticulosViewSet(viewsets.ModelViewSet):
    queryset = Articulos.objects.all()
    serializer_class = ArticulosSerializer
