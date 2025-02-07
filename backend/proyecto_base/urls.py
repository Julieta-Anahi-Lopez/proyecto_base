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
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'tipo-rubros', TipoRubrosViewSet, basename='tipo-rubros')
router.register(r'articulos', ArticulosViewSet, basename='articulos')
router.register(r'tipo-subrubros', TipoSubrubrosViewSet, basename='tipo-subrubros')
router.register(r'tipo-rubros-con-subrubros', TipoRubrosWithSubrubrosViewSet, basename='tipo-rubros-con-subrubros')
router.register(r'tipo-marcas', TipoMarcasViewSet, basename='tipo-marcas')
router.register(r'imagenes', ImagenesViewSet, basename='imagenes')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

