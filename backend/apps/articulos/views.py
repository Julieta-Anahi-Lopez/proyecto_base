from rest_framework import viewsets
from .models import Articulos, Imagenes
from .serializers import ArticulosSerializer, ImagenesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import OuterRef, Subquery
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from apps.categorias.models import TipoRubros, TipoSubrubros, TipoMarcas


class ArticulosViewSet(viewsets.ModelViewSet):
    serializer_class = ArticulosSerializer
    filter_backends = [DjangoFilterBackend]  # Habilitamos los filtros

        
class ArticulosViewSet(viewsets.ModelViewSet):
    serializer_class = ArticulosSerializer
    filter_backends = [DjangoFilterBackend]  # Habilitamos los filtros

    def get_queryset(self):
        print("\n🔍 **Iniciando filtrado de artículos...**\n")

        queryset = Articulos.objects.all()
        print(f"📌 Total de artículos en la base de datos: {queryset.count()}\n")

        # Obtener los parámetros de la URL
        nrogru = self.request.query_params.get('nrogru', None)
        nrosub = self.request.query_params.get('nrosub', None)
        nromar = self.request.query_params.get('nromar', None)
        precio_min = self.request.query_params.get('precio_min', None)
        precio_max = self.request.query_params.get('precio_max', None)
        codigo = self.request.query_params.get('codigo', None)
        nombre = self.request.query_params.get('nombre', None)
        observ = self.request.query_params.get('observ', None)

        print(f"🎯 **Parámetros recibidos en la URL:**")
        print(f"   🏷️ nrogru: {nrogru}")
        print(f"   🏷️ nrosub: {nrosub}")
        print(f"   🏷️ nromar: {nromar}")
        print(f"   💰 precio_min: {precio_min}")
        print(f"   💰 precio_max: {precio_max}")
        print(f"   🔢 codigo: {codigo}")
        print(f"   🏷️ nombre: {nombre}")
        print(f"   📝 observ: {observ}\n")

        # Aplicar filtros si los parámetros están presentes
        if nrogru is not None and nrosub is None:
            print("🔄 Buscando código de TipoRubros...")
            nrogru = TipoRubros.objects.filter(nombre__icontains=nrogru).first()
            if nrogru:
                nrogru = nrogru.codigo
                queryset = queryset.filter(nrogru=nrogru)
                print(f"✅ Filtro aplicado: nrogru = {nrogru}\n")
            else:
                print("❌ No se encontró un TipoRubro con ese nombre.\n")

        if nrogru is not None and nrosub is not None:
            print("🔄 Buscando código de TipoRubros y TipoSubrubros...")
            nrogru = TipoRubros.objects.filter(nombre__icontains=nrogru).first()
            nrosub = TipoSubrubros.objects.filter(nombre__icontains=nrosub).first()

            if nrogru and nrosub:
                nrogru = nrogru.codigo
                nrosub = nrosub.codigo
                queryset = queryset.filter(nrogru=nrogru, nrosub=nrosub)
                print(f"✅ Filtro aplicado: nrogru = {nrogru}, nrosub = {nrosub}\n")
            else:
                print("❌ No se encontró el TipoRubro o el TipoSubrubro indicado.\n")

        if nromar is not None:
            print("🔄 Buscando código de TipoMarcas...")
            nromar = TipoMarcas.objects.filter(nombre__icontains=nromar).first()
            if nromar:
                nromar = nromar.codigo
                queryset = queryset.filter(nromar=nromar)
                print(f"✅ Filtro aplicado: nromar = {nromar}\n")
            else:
                print("❌ No se encontró un TipoMarca con ese nombre.\n")

        if precio_min is not None:
            queryset = queryset.filter(precio__gte=precio_min)
            print(f"✅ Filtro aplicado: precio >= {precio_min}\n")

        if precio_max is not None:
            queryset = queryset.filter(precio__lte=precio_max)
            print(f"✅ Filtro aplicado: precio <= {precio_max}\n")

        if codigo is not None:
            queryset = queryset.filter(codigo__icontains=codigo)
            print(f"✅ Filtro aplicado: código contiene '{codigo}'\n")

        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
            print(f"✅ Filtro aplicado: nombre contiene '{nombre}'\n")

        if observ is not None:
            queryset = queryset.filter(observ__icontains=observ)
            print(f"✅ Filtro aplicado: observación contiene '{observ}'\n")

        print(f"📊 **Total de artículos después del filtrado: {queryset.count()}**\n")
        
        imagenes = Imagenes.objects.all()        

        imagenes_dict = {}
        for img in imagenes:
            
            if img.codimg not in imagenes_dict:
                imagenes_dict[img.codimg] = []
            imagenes_dict[img.codimg].append(img)
        # Agregar las imágenes a los artículos en memoria
        for q in queryset:
            q.imagenes_cache = imagenes_dict.get(q.codigo, [])  # Guardar imágenes en memoria
            
        print("✅ **Filtrado completado. Retornando QuerySet...** 🚀\n")
        return queryset


    
    # @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        print(f"HEADERSSSSS:{request.headers}")
        return super().list(request, *args, **kwargs)

    
    
    
    
    
class ImagenesViewSet(viewsets.ModelViewSet):
    queryset = Imagenes.objects.all()
    serializer_class = ImagenesSerializer



