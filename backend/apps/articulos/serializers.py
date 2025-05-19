from rest_framework import serializers
from .models import Articulos, Imagenes, VistaArticulos
from django.conf import settings

class ArticulosAutenticatedSerializer(serializers.ModelSerializer):
    imagenes = serializers.SerializerMethodField()

    def get_imagenes(self, obj):
            """
            Usa las imágenes cargadas en memoria en lugar de hacer consultas adicionales.
            """
            request = self.context.get('request')

            # print(f"REQUEST EN EL SERIALIZER: {request.__dict__}")
            # TO DO: Resolver porque el retriev no busca correctamnte las imagenes asociadas al objeto. Si busco por codigo via query_param funciona perfectamente
            # Acceder a las imágenes cargadas en la vista
            # print(f"OBJ EN EL SERIALIZER: {obj}")
            imagenes = getattr(obj, 'imagenes_cache', [])            
            # print(f"IMAGENES EN EL SERIALIZER: {imagenes}")
            imagenes_dict = {}

            for i, img in enumerate(imagenes, start=1):
                key = f"foto_{i}"  # foto_1, foto_2, etc.
                imagenes_dict[key] = request.build_absolute_uri(f"{settings.MEDIA_URL}Imagenes/{img.nomarc}") if request else f"{settings.MEDIA_URL}Imagenes/{img.nomarc}"

            return [imagenes_dict] if imagenes_dict else []
        
    
    class Meta:
        model = VistaArticulos
        fields = '__all__'  


class ArticulosSerializer(serializers.ModelSerializer):
    imagenes = serializers.SerializerMethodField()

    def get_imagenes(self, obj):
            """
            Usa las imágenes cargadas en memoria en lugar de hacer consultas adicionales.
            """
            request = self.context.get('request')

            # print(f"REQUEST EN EL SERIALIZER: {request.__dict__}")
            # TO DO: Resolver porque el retriev no busca correctamnte las imagenes asociadas al objeto. Si busco por codigo via query_param funciona perfectamente
            # Acceder a las imágenes cargadas en la vista
            # print(f"OBJ EN EL SERIALIZER: {obj}")
            imagenes = getattr(obj, 'imagenes_cache', [])            
            # print(f"IMAGENES EN EL SERIALIZER: {imagenes}")
            imagenes_dict = {}

            for i, img in enumerate(imagenes, start=1):
                key = f"foto_{i}"  # foto_1, foto_2, etc.
                imagenes_dict[key] = request.build_absolute_uri(f"{settings.MEDIA_URL}Imagenes/{img.nomarc}") if request else f"{settings.MEDIA_URL}Imagenes/{img.nomarc}"

            return [imagenes_dict] if imagenes_dict else []
        
    
    class Meta:
        model = VistaArticulos
        fields = ['codigo', 'nombre', 'nrogru', 'nrosub', 'observ', 'nromar', 'cantidad', 'imagenes']
        
        
        
class ImagenesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagenes
        fields = '__all__'


# class VistaArticulosSerializer(serializers.ModelSerializer):
#      class Meta:
#           model = VistaArticulos
#           fields = '__all__'
          