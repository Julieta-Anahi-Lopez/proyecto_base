from rest_framework import serializers
from .models import Contactos, WebUsuarios
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken


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
    # contacto = ContactosSerializer()

    class Meta:
        model = WebUsuarios
        fields = '__all__'

    # def create(self, validated_data):
    #     # Extraemos los datos del contacto
    #     contacto_data = validated_data.pop('contacto')
        
    #     # Creamos el contacto primero
    #     contacto = Contactos.objects.create(**contacto_data)

    #         # Creamos el usuario web, asociando el nro_contacto al ID del contacto
    #     validated_data['nro_contacto'] = contacto.id
    #     web_usuario = WebUsuarios.objects.create(**validated_data)
        
    #     return web_usuario

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializador personalizado para obtener tokens JWT iniciales
    """
    @classmethod
    def get_token(cls, user):
        # Obtener el token con la clase base
        token = RefreshToken.for_user(user)
        
        # Personalizar los claims del token si es necesario
        token['email'] = user.e_mail
        token['catusu'] = user.catusu
        
        return token

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Serializador personalizado para refrescar tokens JWT
    """
    def validate(self, attrs):
        try:
            # Obtener el token de refresco
            refresh = RefreshToken(attrs['refresh'])
            
            # Extraer el ID del usuario del token
            user_id = refresh['user_id']
            
            # Verificar que el usuario existe
            WebUsuarios.objects.get(codigo=user_id)
            
            # Si el usuario existe, generar un nuevo token de acceso
            return {
                'access': str(refresh.access_token)
            }
        except WebUsuarios.DoesNotExist:
            raise serializers.ValidationError("Token inválido o usuario no encontrado")
        except Exception as e:
            raise serializers.ValidationError(f"Error al refrescar token: {str(e)}")








