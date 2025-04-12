from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import WebUsuarios
from rest_framework.exceptions import AuthenticationFailed


class CustomAuth(JWTAuthentication):
    """
Autenticador personalizado para los usuarios web.
Extiende la autenticación JWT estándar para trabajar con nuestro modelo WebUsuarios.
"""
    def authenticate(self, request):
        # Usar la autenticación JWT estándar para obtener y validar el header
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        # Validar el token
        validated_token = self.get_validated_token(raw_token)
        
        # Obtener el ID del usuario del token
        codigo = validated_token.get('user_id')
        
        try:
            # Buscar el usuario web por su código
            user = WebUsuarios.objects.get(codigo=codigo)
            return (user, validated_token)
        except WebUsuarios.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado')



