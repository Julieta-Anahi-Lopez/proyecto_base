from rest_framework import serializers
from .models import Contactos, WebUsuarios


class ContactosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactos
        fields = '__all__'
        read_only_fields = ['id']


class WebUsuariosListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebUsuarios
        fields = '__all__'

class WebUsuariosCreateUpdateSerializer(serializers.ModelSerializer):
    contacto = ContactosSerializer()

    class Meta:
        model = WebUsuarios
        fields = '__all__'

    def create(self, validated_data):
        # Extraemos los datos del contacto
        contacto_data = validated_data.pop('contacto')
        
        # Creamos el contacto primero
        contacto = Contactos.objects.create(**contacto_data)

            # Creamos el usuario web, asociando el nro_contacto al ID del contacto
        validated_data['nro_contacto'] = contacto.id
        web_usuario = WebUsuarios.objects.create(**validated_data)
        
        return web_usuario

