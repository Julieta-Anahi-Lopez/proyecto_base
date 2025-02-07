from rest_framework import serializers
from .models import Articulos, Imagenes
from django.conf import settings

class ArticulosSerializer(serializers.ModelSerializer):
    imagenes = serializers.SerializerMethodField()

    def get_imagenes(self, obj):
            """
            Usa las imágenes cargadas en memoria en lugar de hacer consultas adicionales.
            """
            request = self.context.get('request')

            # Acceder a las imágenes cargadas en la vista
            imagenes = getattr(obj, 'imagenes_cache', [])

            imagenes_dict = {}
            for i, img in enumerate(imagenes, start=1):
                key = f"foto_{i}"  # foto_1, foto_2, etc.
                imagenes_dict[key] = request.build_absolute_uri(f"{settings.MEDIA_URL}Imagenes/{img.nomarc}") if request else f"{settings.MEDIA_URL}Imagenes/{img.nomarc}"

            return [imagenes_dict] if imagenes_dict else []
        
    
    class Meta:
        model = Articulos
        fields = '__all__'  
        
        
        
class ImagenesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagenes
        fields = '__all__'