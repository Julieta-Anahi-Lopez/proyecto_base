# backend/apps/pedidos/views_usuario.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db import connection
from django.db.models import Q
from datetime import datetime, timedelta

from .models import Pedidos, PedidosDetalle
from .serializers import PedidosSerializer
from apps.users.models import WebUsuarios

class PedidosPaginacion(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PedidosPorUsuarioView(APIView):
    """
    Vista independiente para consultar pedidos por usuario.
    Esta vista está separada del ViewSet principal de Pedidos.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = PedidosPaginacion

    def get(self, request, format=None):
        """
        Obtiene los pedidos del usuario autenticado con opciones de filtrado.
        """
        # Obtener el usuario actual
        user = request.user
        
        # Parámetros de filtrado
        fecha_desde = request.query_params.get('fecha_desde', None)
        fecha_hasta = request.query_params.get('fecha_hasta', None)
        estado = request.query_params.get('estado', None)
        comprobante = request.query_params.get('comprobante', None)
        orden = request.query_params.get('orden', '-fecped')  # Por defecto, más reciente primero
        
        # Construir la consulta base
        queryset = Pedidos.objects.filter(nrocli=user.codigo)
        
        # Aplicar filtros si se proporcionan
        if fecha_desde:
            try:
                fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
                queryset = queryset.filter(fecped__gte=fecha_desde)
            except ValueError:
                return Response(
                    {"error": "Formato de fecha_desde inválido. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if fecha_hasta:
            try:
                fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
                # Ajustar al final del día
                fecha_hasta = fecha_hasta + timedelta(days=1, microseconds=-1)
                queryset = queryset.filter(fecped__lte=fecha_hasta)
            except ValueError:
                return Response(
                    {"error": "Formato de fecha_hasta inválido. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if estado:
            # Nota: Ajustar según el campo real que indique el estado en el modelo
            queryset = queryset.filter(nroest=estado)
        
        if comprobante:
            queryset = queryset.filter(compro__icontains=comprobante)
        
        # Aplicar ordenamiento
        if orden.startswith('-'):
            orden_campo = orden[1:]
            queryset = queryset.order_by(f"-{orden_campo}")
        else:
            queryset = queryset.order_by(orden)
        
        # Aplicar paginación
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        
        # Serializar los resultados
        serializer = PedidosSerializer(result_page, many=True)
        
        # Devolver respuesta paginada
        return paginator.get_paginated_response(serializer.data)

class PedidoDetalleUsuarioView(APIView):
    """
    Vista para obtener el detalle de un pedido específico para un usuario.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, comprobante, format=None):
        """
        Obtiene los detalles de un pedido específico si pertenece al usuario autenticado.
        """
        user = request.user
        
        # Verificar que el pedido existe y pertenece al usuario
        try:
            pedido = Pedidos.objects.get(compro=comprobante, nrocli=user.codigo)
        except Pedidos.DoesNotExist:
            return Response(
                {"error": "Pedido no encontrado o no tiene permisos para verlo"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serializar el pedido con sus detalles
        serializer = PedidosSerializer(pedido)
        
        return Response(serializer.data)

class ResumenPedidosUsuarioView(APIView):
    """
    Vista para obtener un resumen de los pedidos del usuario.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        """
        Obtiene estadísticas resumidas de los pedidos del usuario.
        """
        user = request.user
        
        # Obtener todos los pedidos del usuario
        pedidos = Pedidos.objects.filter(nrocli=user.codigo)
        
        # Calcular estadísticas
        total_pedidos = pedidos.count()
        
        # Pedidos recientes (últimos 30 días)
        fecha_reciente = datetime.now() - timedelta(days=30)
        pedidos_recientes = pedidos.filter(fecped__gte=fecha_reciente).count()
        
        # Otros cálculos de estadísticas según las necesidades
        # Por ejemplo, podríamos contar por estado si hay un campo de estado
        
        # Preparar respuesta
        data = {
            'total_pedidos': total_pedidos,
            'pedidos_recientes': pedidos_recientes,
            'cliente': {
                'codigo': user.codigo,
                'nombre': user.nombre
            }
        }
        
        return Response(data)