from rest_framework import viewsets
from .models import Articulos, Imagenes, VistaArticulos
from .serializers import ArticulosAutenticatedSerializer,ArticulosSerializer, ImagenesSerializer#, VistaArticulosSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import OuterRef, Subquery
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from apps.categorias.models import TipoRubros, TipoSubrubros, TipoMarcas
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Case, When, IntegerField
from apps.users.models import Contactos



# class ArticulosViewSet(viewsets.ModelViewSet):
#     serializer_class = ArticulosSerializer
#     filter_backends = [DjangoFilterBackend]  # Habilitamos los filtros

        
class ArticulosViewSet(viewsets.ModelViewSet):
    serializer_class = ArticulosAutenticatedSerializer
    filter_backends = [DjangoFilterBackend]  # Habilitamos los filtros
    # permission_classes = [AllowAny]
    
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user


        contacto = None
        if user.is_authenticated:
            contacto = Contactos.objects.filter(nrocon=user.codigo).first()
        context['contacto'] = contacto
        return context
    
    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return ArticulosAutenticatedSerializer
        return ArticulosSerializer


    def get_queryset(self):

        if self.action == 'retrieve':
            instance = VistaArticulos.objects.filter(codigo=self.kwargs['pk']).first()
            print(f"Objeto encontrado: {instance}")


        elif self.action == 'list':
            print("\n🔍 **Iniciando filtrado de artículos...**\n")

            

            queryset = VistaArticulos.objects.annotate(
                prioridad=Case(
                    When(nromar=6, then=0),
                    default=1,
                    output_field=IntegerField()
                )
            ).order_by('prioridad', 'nromar', '-stock')
            print(f"📌 Total de artículos en la base de datos: {queryset.count()}\n")

            # Obtener los parámetros de la URL
            rubro = self.request.query_params.get('nrogru', None)
            subrubro = self.request.query_params.get('nrosub', None)
            nromar = self.request.query_params.get('nromar', None)
            precio_min = self.request.query_params.get('precio_min', None)
            precio_max = self.request.query_params.get('precio_max', None)
            codigo = self.request.query_params.get('codigo', None)
            nombre = self.request.query_params.get('nombre', None)
            observ = self.request.query_params.get('observ', None)

            print(f"🎯 **Parámetros recibidos en la URL:**")
            print(f"   🏷️ nrogru: {rubro}")
            print(f"   🏷️ nrosub: {subrubro}")
            print(f"   🏷️ nromar: {nromar}")
            print(f"   💰 precio_min: {precio_min}")
            print(f"   💰 precio_max: {precio_max}")
            print(f"   🔢 codigo: {codigo}")
            print(f"   🏷️ nombre: {nombre}")
            print(f"   📝 observ: {observ}\n")

            # ahora los parametros estan en la vista de nro gru, la tabla que consumo los tiene, asique filtro directamente el queryset
            # Aplicar filtros si los parámetros están presentes
            if rubro is not None and subrubro is None:
                print("🔄 Buscando código de TipoRubros...")
                queryset = queryset.filter(rubro=rubro)
                print(f"✅ Filtro aplicado: rubro = {rubro}\n")
                
                # nrogru = TipoRubros.objects.filter(nombre__icontains=nrogru).first()
                # if nrogru:
                #     nrogru = nrogru.codigo
                #     queryset = queryset.filter(nrogru=nrogru)
                # else:
                #     print("❌ No se encontró un TipoRubro con ese nombre.\n")

            if rubro is not None and subrubro is not None:
                print("🔄 Buscando código de TipoRubros y TipoSubrubros...")
                queryset = queryset.filter(rubro=rubro, nrosub=subrubro)
                print(f"✅ Filtro aplicado: nrogru = {rubro}, nrosub = {subrubro}\n")
                # nrogru = TipoRubros.objects.filter(nombre__icontains=nrogru).first()
                # nrosub = TipoSubrubros.objects.filter(nombre__icontains=nrosub).first()

                # if nrogru and nrosub:
                #     nrogru = nrogru.codigo
                #     nrosub = nrosub.codigo
                #     queryset = queryset.filter(nrogru=nrogru, nrosub=nrosub)
                #     print(f"✅ Filtro aplicado: nrogru = {nrogru}, nrosub = {nrosub}\n")
                # else:
                #     print("❌ No se encontró el TipoRubro o el TipoSubrubro indicado.\n")

            if nromar is not None:
                
                print("🔄 Buscando código de TipoMarcas...")
                queryset = queryset.filter(nromar=nromar)
                
                # nromar = TipoMarcas.objects.filter(nombre__icontains=nromar).first()
                # if nromar:
                #     nromar = nromar.codigo
                #     queryset = queryset.filter(nromar=nromar)
                #     print(f"✅ Filtro aplicado: nromar = {nromar}\n")
                # else:
                #     print("❌ No se encontró un TipoMarca con ese nombre.\n")

            if precio_min is not None:
                queryset = queryset.filter(publico__gte=precio_min)
                print(f"✅ Filtro aplicado: precio >= {precio_min}\n")

            if precio_max is not None:
                queryset = queryset.filter(publico__lte=precio_max)
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


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user.is_authenticated:
            print("Usuario autenticado")
        else:
            print("Usuario no autenticado")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)






    
    # @method_decorator(cache_page(60 * 60 * 2))
    # def list(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         print("Usuario autenticado")
    #         serializer = ArticulosAutenticatedSerializer(self.get_queryset(), many=True, context={'request': request})
    #         return Response(serializer.data)
    #     else:
    #         print("Usuario no autenticado")
    #         serializer = ArticulosSerializer(self.get_queryset(), many=True, context={'request': request})
    #         return Response(serializer.data)
    #     # return super().list(request, *args, **kwargs)
    
    # def retrieve(self, request, *args, **kwargs):
    #     print("En el retrieve")
    #     instance = VistaArticulos.objects.filter(codigo=self.kwargs['pk']).first()
    #     print(f"Objeto encontrado: {instance}")
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    
    
    
    
    
class ImagenesViewSet(viewsets.ModelViewSet):
    queryset = Imagenes.objects.all()
    serializer_class = ImagenesSerializer


# class VistaArticulosViewSet(viewsets.ModelViewSet):
#     queryset = VistaArticulos.objects.all()
#     serializer_class = VistaArticulosSerializer
#     permission_classes = [AllowAny]



