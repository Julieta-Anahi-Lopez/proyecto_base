import django_filters
from .models import Articulos

class ArticuloFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')  # Buscar por coincidencia parcial
    observ = django_filters.CharFilter(lookup_expr='icontains')  # También para observaciones

    class Meta:
        model = Articulos
        fields = ['nrogru', 'nrosub', 'precio', 'codigo', 'nombre', 'observ']
