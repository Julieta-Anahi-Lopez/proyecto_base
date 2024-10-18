# backend/proyecto_base/views.py

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def prueba_conexion(request):
    return Response({"mensaje": "Conexión exitosa con el backend"}, status=200)
