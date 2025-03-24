from rest_framework import serializers
from .models import Pedidos, PedidosDetalle

class PedidosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = '__all__'


class PedidosDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidosDetalle
        fields = '__all__'