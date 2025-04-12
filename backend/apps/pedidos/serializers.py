from rest_framework import serializers
from .models import Pedidos, PedidosDetalle
from apps.articulos.models import Articulos
from django.db import connection

class PedidoDetalleInputSerializer(serializers.Serializer):
    """
    Serializer para validar y procesar cada ítem de detalle del pedido al crear
    """
    codigo = serializers.CharField(required=True, help_text="Código del artículo")
    cantidad = serializers.FloatField(required=True, help_text="Cantidad del artículo")
    precio = serializers.FloatField(required=True, help_text="Precio del artículo")
    descuento = serializers.FloatField(required=False, default=0, help_text="Porcentaje de descuento")
    observacion = serializers.CharField(required=False, default="", help_text="Observaciones específicas del ítem")
    nrolis = serializers.IntegerField(required=False, default=0, help_text="Número de lista de precios")

    def validate_codigo(self, value):
        # Verificar que el código del artículo exista
        articulo = Articulos.objects.filter(codigo=value).first()
        if not articulo:
            raise serializers.ValidationError(f"El artículo con código {value} no existe")
        return value

    def validate_cantidad(self, value):
        # Validar que la cantidad sea mayor que cero
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que cero")
        return value

    def validate_precio(self, value):
        # Validar que el precio sea mayor o igual a cero
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return value


class PedidosCreateSerializer(serializers.Serializer):
    """
    Serializer para la creación de pedidos con sus detalles
    """
    observ = serializers.CharField(required=False, default="", help_text="Observaciones generales del pedido")
    detalle = PedidoDetalleInputSerializer(many=True, required=True, help_text="Detalles del pedido")

    def validate_detalle(self, value):
        # Validar que hay al menos un detalle
        if not value:
            raise serializers.ValidationError("El pedido debe contener al menos un ítem de detalle")
        return value


# Cambiado de ModelSerializer a Serializer
class PedidosDetalleSerializer(serializers.Serializer):
    """
    Serializer para mostrar los detalles de un pedido - usando Serializer en lugar de ModelSerializer
    """
    compro = serializers.CharField()
    nroord = serializers.IntegerField() 
    codart = serializers.CharField()
    cantid = serializers.FloatField()
    descri = serializers.CharField()
    penden = serializers.FloatField()
    pendfc = serializers.FloatField()
    precio = serializers.FloatField()
    nrolis = serializers.IntegerField()
    pordes = serializers.FloatField()
    nroemp = serializers.IntegerField()
    observ = serializers.CharField()
    poruni = serializers.FloatField()


class PedidosSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar pedidos
    """
    detalles = serializers.SerializerMethodField()

    class Meta:
        model = Pedidos
        fields = '__all__'
    
    def get_detalles(self, obj):
        """
        Obtiene los detalles asociados a un pedido usando SQL nativo
        para evitar problemas con el ORM de Django
        """
        try:
            # Utilizar SQL nativo para obtener los detalles
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        compro, nroord, codart, cantid, descri, penden, 
                        pendfc, precio, nrolis, pordes, nroemp, observ, poruni 
                    FROM pedidos_detalle 
                    WHERE compro = %s AND nroemp = %s
                """, [obj.compro, obj.nroemp])
                
                # Convertir los resultados a una lista de diccionarios
                columns = [col[0] for col in cursor.description]
                detalles_list = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            
            # Serializar la lista de diccionarios
            return PedidosDetalleSerializer(detalles_list, many=True).data
        
        except Exception as e:
            print(f"Error en get_detalles: {str(e)}")
            return []  #



# from rest_framework import serializers
# from .models import Pedidos, PedidosDetalle
# from apps.articulos.models import Articulos

# class PedidoDetalleInputSerializer(serializers.Serializer):
#     """
#     Serializer para validar y procesar cada ítem de detalle del pedido al crear
#     """
#     codigo = serializers.CharField(required=True, help_text="Código del artículo")
#     cantidad = serializers.FloatField(required=True, help_text="Cantidad del artículo")
#     precio = serializers.FloatField(required=True, help_text="Precio del artículo")
#     descuento = serializers.FloatField(required=False, default=0, help_text="Porcentaje de descuento")
#     observacion = serializers.CharField(required=False, default="", help_text="Observaciones específicas del ítem")
#     nrolis = serializers.IntegerField(required=False, default=0, help_text="Número de lista de precios")

#     def validate_codigo(self, value):
#         # Verificar que el código del artículo exista
#         articulo = Articulos.objects.filter(codigo=value).first()
#         if not articulo:
#             raise serializers.ValidationError(f"El artículo con código {value} no existe")
#         return value

#     def validate_cantidad(self, value):
#         # Validar que la cantidad sea mayor que cero
#         if value <= 0:
#             raise serializers.ValidationError("La cantidad debe ser mayor que cero")
#         return value

#     def validate_precio(self, value):
#         # Validar que el precio sea mayor o igual a cero
#         if value < 0:
#             raise serializers.ValidationError("El precio no puede ser negativo")
#         return value


# class PedidosCreateSerializer(serializers.Serializer):
#     """
#     Serializer para la creación de pedidos con sus detalles
#     """
#     observ = serializers.CharField(required=False, default="", help_text="Observaciones generales del pedido")
#     detalle = PedidoDetalleInputSerializer(many=True, required=True, help_text="Detalles del pedido")

#     def validate_detalle(self, value):
#         # Validar que hay al menos un detalle
#         if not value:
#             raise serializers.ValidationError("El pedido debe contener al menos un ítem de detalle")
#         return value


# class PedidosDetalleSerializer(serializers.ModelSerializer):
#     """
#     Serializer para mostrar los detalles de un pedido
#     """
#     class Meta:
#         model = PedidosDetalle
#         fields = ['compro', 'nroord', 'codart', 'cantid', 'descri', 'penden', 
#          'pendfc', 'precio', 'nrolis', 'pordes', 'nroemp', 'observ', 'poruni']


# class PedidosSerializer(serializers.ModelSerializer):
#     """
#     Serializer para mostrar pedidos
#     """
#     detalles = serializers.SerializerMethodField()

#     class Meta:
#         model = Pedidos
#         fields = '__all__'
    
#     def get_detalles(self, obj):
#         """
#         Obtiene los detalles asociados a un pedido
#         """
#         detalles = PedidosDetalle.objects.filter(compro=obj.compro, nroemp=obj.nroemp)
#         print("GET DETALLES EN SERIALIZER: ", PedidosDetalleSerializer(detalles, many=True))
#         return PedidosDetalleSerializer(detalles, many=True).data


















# # from rest_framework import serializers
# # from .models import Pedidos, PedidosDetalle

# # class PedidosSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Pedidos
# #         fields = '__all__'


# # class PedidosDetalleSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = PedidosDetalle
# #         fields = '__all__'