from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PedidosSerializer
from .models import Pedidos
# from rest_framework.permissions import AllowAny

# Create your views here.
class PedidosViewSet(ModelViewSet):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosSerializer
    permission_classes = []