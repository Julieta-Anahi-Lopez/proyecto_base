from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import TipoRubros
from .serializers import TipoRubrosSerializer, TipoSubrubrosSerializer, TipoRubrosWithSubrubrosSerializer, TipoMarcasSerializer
from .models import TipoSubrubros, TipoMarcas
from rest_framework import generics
from rest_framework.permissions import AllowAny


class TipoRubrosViewSet(viewsets.ReadOnlyModelViewSet):  # Solo permite GET
    serializer_class = TipoRubrosSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return TipoRubros.objects.filter(verweb='1')  # Filtra solo los registros donde verweb='1'





class TipoSubrubrosViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet que maneja TipoSubrubros con clave primaria compuesta (nrorub, codigo).
    """
    serializer_class = TipoSubrubrosSerializer
    queryset = TipoSubrubros.objects.all()
    lookup_url_kwarg = 'nrorub_codigo'  # Necesario para capturar el parámetro en la URL

    def get_object(self):
        """
        Personaliza la recuperación de un objeto usando `nrorub` y `codigo`.
        """
        lookup_value = self.kwargs.get("nrorub_codigo")

        if lookup_value is None:
            raise ValueError("El parámetro 'nrorub_codigo' no fue recibido correctamente en la URL.")

        try:
            nrorub, codigo = lookup_value.split("-")
        except ValueError:
            raise ValueError(f"El valor '{lookup_value}' no es válido. Debe estar en formato 'nrorub-codigo'.")

        return get_object_or_404(TipoSubrubros, nrorub=nrorub, codigo=codigo)





class TipoRubrosWithSubrubrosViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet que devuelve TipoRubros con sus TipoSubrubros anidados.
    """
    queryset = TipoRubros.objects.filter(verweb='1')
    serializer_class = TipoRubrosSerializer  # Usamos el serializer original para TipoRubros
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        """
        Sobreescribe el método list para incluir los TipoSubrubros de cada TipoRubro.
        """
        rubros = TipoRubros.objects.filter(verweb='1')
        data = []

        for rubro in rubros:
            subrubros = TipoSubrubros.objects.filter(nrorub=rubro.codigo)  # Relación basada en nrorub = codigo
            subrubros_serializados = TipoSubrubrosSerializer(subrubros, many=True).data  # Serializar los subrubros

            rubro_data = TipoRubrosSerializer(rubro).data  # Serializar el rubro
            rubro_data["subrubros"] = subrubros_serializados  # Agregar los subrubros al diccionario de rubro

            data.append(rubro_data)

        return Response(data)  # Devolver la respuesta en formato JSON




class TipoMarcasViewSet(viewsets.ReadOnlyModelViewSet):  # Solo permite GET
    serializer_class = TipoMarcasSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return TipoMarcas.objects.all()  # Filtra solo los registros donde verweb='1'