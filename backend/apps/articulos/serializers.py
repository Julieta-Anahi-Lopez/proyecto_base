from rest_framework import serializers
from .models import Articulos

class ArticulosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulos
        fields = '__all__'  # O especifica los campos si no quieres exponer todos