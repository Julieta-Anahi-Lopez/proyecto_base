import django_filters
from .models import Articulos

class ArticuloFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')  # Buscar por coincidencia parcial
    observ = django_filters.CharFilter(lookup_expr='icontains')  # También para observaciones
    precio_min = django_filters.NumberFilter(field_name="precio", lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name="precio", lookup_expr='lte')
    class Meta:
        model = Articulos
        fields = ['nrogru', 'nrosub', 'precio', 'codigo', 'nombre', 'observ']
