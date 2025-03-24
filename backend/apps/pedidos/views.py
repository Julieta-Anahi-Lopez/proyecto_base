from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PedidosSerializer, PedidosDetalleSerializer
from .models import Pedidos, PedidosDetalle
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from datetime import datetime
from apps.users.models import Contactos
# from rest_framework.permissions import AllowAny

# Create your views here.
class PedidosViewSet(ModelViewSet):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosSerializer
    permission_classes = []

    def get_serializer_class(self):
        #Por ahora lo dejamos definido asi, luego si es necesario agrego otro.
        return PedidosSerializer


    def get_queryset(self):
        return Pedidos.objects.all()
        #Evaluar agregar despues. Po ahora todos los pedidos
        # return Pedidos.objects.filter(usuario=self.request.user)

    def create(self, request, *args, **kwargs):
        print(f"request.data: {request.data}")
        nro_comprobante = Pedidos.objects.all().order_by('-compro').first()
        print(f"nro_comprobante antes del manejo: {nro_comprobante}")
        # Manejar que nro_comprobante devuelve valores en string de tipo 0002-00001365. Debo generar el consecutivo de eso
        if nro_comprobante:
            nro_comprobante = nro_comprobante.compro
            nro_comprobante = nro_comprobante.split("-")
            nro_comprobante = f"{nro_comprobante[0]}-{int(nro_comprobante[1]) + 1:08}"
        print(f"nro_comprobante: {nro_comprobante}")
        nro_cliente = request.user.codigo
        print(f"nro_cliente: {nro_cliente}")
        fecha_pedido = datetime.now()
        print(f"fecha_pedido: {fecha_pedido}")
        observaciones = request.data['observ']
        print(f"observaciones: {observaciones}")
        nro_usu = 0
        print(f"nro_usu: {nro_usu}")
        nro_vendedor = Contactos.objects.filter(nrocon=nro_cliente).first().nroven
        print(f"nro_vendedor: {nro_vendedor}")
        imputa = 0
        print(f"imputa: {imputa}")
        nombre_pc = 'Sitio Web'
        print(f"nombre_pc: {nombre_pc}")
        nro_emp = 1
        print(f"nro_emp: {nro_emp}")
        tipo_deposito = 1
        print(f"tipo_deposito: {tipo_deposito}")
        nro_est = '0'
        print(f"nro_est: {nro_est}")
        # pedido_detalle = request.data['detalle']
        # print(f"pedido_detalle: {pedido_detalle}")
        # for detalle in pedido_detalle:
        #     print(f"detalle: {detalle}")
        #     print(f"detalle['codigo']: {detalle['codigo']}")
        #     print(f"detalle['cantidad']: {detalle['cantidad']}")
        #     print(f"detalle['precio']: {detalle['precio']}")
        #     print(f"detalle['descuento']: {detalle['descuento']}")
        #     print(f"detalle['total']: {detalle['total']}")


        pedido = {
            'compro': nro_comprobante,
            'nrocli': nro_cliente,
            'fecped': fecha_pedido,
            'plazo': '0',
            'lugent': '0',
            'condic': '0',
            'observ': observaciones,
            'nrousu': nro_usu,
            'nroven': nro_vendedor,
            'imputa': imputa,
            'nombpc': nombre_pc,
            'origen': '0',
            'nroemp': nro_emp,
            'tipdep': tipo_deposito,
            'nroest': nro_est,
        }

        with transaction.atomic():
            try:
                pedido, creado = Pedidos.objects.get_or_create(**pedido)
                if creado:
                    serializer = self.get_serializer(pedido)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                else:
                    return Response({"error": "El pedido ya existe"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # with transaction.atomic():
        #     try:
        #         data = pedido
        #         serializer = self.get_serializer(data=data)
        #         serializer.is_valid(raise_exception=True)
        #         self.perform_create(serializer)
        #         headers = self.get_success_headers(serializer.data)
        #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        #     except Exception as e:
        #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class PedidoDetalleViewSet(ModelViewSet):
    queryset = PedidosDetalle.objects.all()
    serializer_class = PedidosDetalleSerializer
    permission_classes = []

    def get_serializer_class(self):
        #Por ahora lo dejamos definido asi, luego si es necesario agrego otro.
        return PedidosDetalleSerializer

    def get_queryset(self):
        return PedidosDetalle.objects.all()
        #Evaluar agregar despues. Po ahora todos los pedidos
        # return Pedidos.objects.filter(usuario=self.request.user)

