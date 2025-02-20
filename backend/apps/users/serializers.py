from rest_framework import serializers
from .models import Contactos, WebUsuarios


class ContactosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactos
        fields = '__all__'

class WebUsuariosSerializer(serializers.ModelSerializer):


    class Meta:
        model = WebUsuarios
        fields = '__all__'


