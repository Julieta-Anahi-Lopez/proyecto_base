from rest_framework import serializers
from .models import Articulos, Imagenes, VistaArticulos
from django.conf import settings

class ArticulosAutenticatedSerializer(serializers.ModelSerializer):
    imagenes = serializers.SerializerMethodField()
    precio_final = serializers.SerializerMethodField()

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
        
        
    def get_precio_final(self, obj):
        contacto = self.context.get('contacto')
        # print(f"Contacto en el serializer: {contacto}")
        if not contacto:
            return None

        return obj.precio if contacto.nrolis == 0 else obj.lista1

        
    
    class Meta:
        model = VistaArticulos
        fields = [
            'codigo', 'nombre', 'stock', 'costo', 'rubro', 'subrubro',
            'nromar', 'marca', 'imagenes', 'precio_final'
        ] 


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
        fields = ['codigo', 'nombre','stock', 'costo', 'rubro', 'subrubro', 'nromar', 'marca','imagenes']
        
        
        
class ImagenesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagenes
        fields = '__all__'


# class VistaArticulosSerializer(serializers.ModelSerializer):
#      class Meta:
#           model = VistaArticulos
#           fields = '__all__'
          