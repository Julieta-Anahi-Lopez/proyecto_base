# apps/prueba/urls.py

from rest_framework.routers import DefaultRouter
from .views import ArticulosViewSet

router = DefaultRouter()
router.register(r'', ArticulosViewSet)

urlpatterns = router.urls
