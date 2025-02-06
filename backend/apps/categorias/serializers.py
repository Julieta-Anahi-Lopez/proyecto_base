from rest_framework import serializers
from .models import TipoRubros
from .models import TipoSubrubros

class TipoRubrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoRubros
        fields = '__all__'  # Puedes personalizar los campos si es necesario





class TipoSubrubrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSubrubros
        fields = '__all__'  # Puedes personalizar los campos si es necesario
        
        
        


class TipoRubrosWithSubrubrosSerializer(serializers.ModelSerializer):
    subrubros = serializers.SerializerMethodField()  # Campo personalizado para subrubros

    class Meta:
        model = TipoRubros
        fields = ['codigo', 'nombre', 'subrubros']

    def get_subrubros(self, obj):
        """
        Obtiene los TipoSubrubros asociados a este TipoRubro.
        """
        subrubros = TipoSubrubros.objects.filter(nrorub=obj.codigo)  # Filtra por relación
        # from .serializers import TipoSubrubrosSerializer  # Importa sin modificar el original
        return TipoSubrubrosSerializer(subrubros, many=True).data
