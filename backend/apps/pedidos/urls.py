# backend/apps/pedidos/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidosViewSet
from .views_usuarios import PedidosPorUsuarioView, PedidoDetalleUsuarioView, ResumenPedidosUsuarioView

# Router para los ViewSets
router = DefaultRouter()
router.register(r'', PedidosViewSet)

# URLs específicas para las vistas de pedidos por usuario
pedidos_usuario_urlpatterns = [
    path('mis-pedidos/', PedidosPorUsuarioView.as_view(), name='mis-pedidos'),
    path('mis-pedidos/<str:comprobante>/', PedidoDetalleUsuarioView.as_view(), name='detalle-pedido'),
    path('mis-pedidos-resumen/', ResumenPedidosUsuarioView.as_view(), name='resumen-pedidos'),
]

# Combinando todas las URLs
urlpatterns = [
    path('', include(router.urls)),
    path('usuario/', include(pedidos_usuario_urlpatterns)),
]