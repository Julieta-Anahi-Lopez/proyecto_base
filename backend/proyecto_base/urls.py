"""proyecto_base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.categorias.views import TipoRubrosViewSet, TipoSubrubrosViewSet, TipoRubrosWithSubrubrosViewSet, TipoMarcasViewSet
from apps.articulos.views import ArticulosViewSet, ImagenesViewSet
from apps.users.views import ContactosViewSet, WebUsuariosViewSet
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import LoginView, CustomTokenRefreshView
from apps.pedidos.views import PedidosViewSet

router = DefaultRouter()
router.register(r'tipo-rubros', TipoRubrosViewSet, basename='tipo-rubros')
router.register(r'articulos', ArticulosViewSet, basename='articulos')
router.register(r'tipo-subrubros', TipoSubrubrosViewSet, basename='tipo-subrubros')
router.register(r'tipo-rubros-con-subrubros', TipoRubrosWithSubrubrosViewSet, basename='tipo-rubros-con-subrubros')
router.register(r'tipo-marcas', TipoMarcasViewSet, basename='tipo-marcas')
router.register(r'imagenes', ImagenesViewSet, basename='imagenes')
router.register(r'contactos', ContactosViewSet, basename='contactos')
router.register(r'web-usuarios', WebUsuariosViewSet, basename='web_usuarios')
router.register(r'pedidos', PedidosViewSet, basename='pedidos')

# Rutas para autenticación
auth_urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
     path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]





urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),    
    path('api/auth/', include(auth_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

