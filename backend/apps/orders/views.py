from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.utils import timezone
from .models import Pedido, DetallePedido, PedidoMesero, Pago
from .serializers import PedidoSerializer, DetallePedidoSerializer, PedidoMeseroSerializer, PagoSerializer
from apps.users.permissions import IsAdmin, IsAdminOCajero, IsMesero
from apps.inventory.models import Producto, TransaccionInventario


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by("-created_at")
    serializer_class = PedidoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["id_mesa", "estado", "id_mesa__id_sucursal"]
    search_fields = ["id_mesa__numero"]
    ordering_fields = ["created_at", "total"]

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [IsMesero | IsAdmin]  # Solo meseros y admin pueden crear pedidos
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]  # Solo admin puede modificar/eliminar
        else:
            permission_classes = [IsAdminOCajero | IsMesero]  # Todos pueden ver los pedidos
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # Validar que la mesa esté disponible
        mesa_id = request.data.get("id_mesa")

        from apps.sucursales.models import Mesa

        try:
            mesa = Mesa.objects.get(id_mesa=mesa_id)
            if mesa.estado != "libre":
                return Response(
                    {"error": "La mesa seleccionada no está disponible"}, status=status.HTTP_400_BAD_REQUEST
                )
        except Mesa.DoesNotExist:
            return Response({"error": "La mesa seleccionada no existe"}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el pedido
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            pedido = serializer.save(estado="pendiente")

            # Crear la relación con el mesero
            PedidoMesero.objects.create(id_pedido=pedido, id_mesero=request.user)

            # Actualizar el estado de la mesa
            mesa.estado = "ocupada"
            mesa.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["post"])
    def cambiar_estado(self, request, pk=None):
        pedido = self.get_object()
        nuevo_estado = request.data.get("estado")

        if nuevo_estado not in [choice[0] for choice in Pedido.STATUS_CHOICES]:
            return Response({"error": "Estado inválido"}, status=status.HTTP_400_BAD_REQUEST)

        # Validar transiciones de estado
        if pedido.estado == "pagado" and nuevo_estado != "pagado":
            return Response(
                {"error": "No se puede cambiar el estado de un pedido pagado"}, status=status.HTTP_400_BAD_REQUEST
            )

        pedido.estado = nuevo_estado
        pedido.save()

        return Response({"status": "Estado actualizado exitosamente"})


class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id_pedido", "id_producto"]

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [IsMesero | IsAdmin]  # Solo meseros y admin pueden agregar items
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]  # Solo admin puede modificar/eliminar
        else:
            permission_classes = [IsAdminOCajero | IsMesero]  # Todos pueden ver los detalles
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # Verificar que el pedido exista y no esté pagado
        pedido_id = request.data.get("id_pedido")
        try:
            pedido = Pedido.objects.get(id_pedido=pedido_id)
            if pedido.estado == "pagado":
                return Response(
                    {"error": "No se pueden agregar productos a un pedido pagado"}, status=status.HTTP_400_BAD_REQUEST
                )
        except Pedido.DoesNotExist:
            return Response({"error": "El pedido seleccionado no existe"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar stock del producto
        producto_id = request.data.get("id_producto")
        cantidad = int(request.data.get("cantidad", 1))

        try:
            producto = Producto.objects.get(id_producto=producto_id)

            # Buscar el inventario en la sucursal de la mesa
            from apps.inventory.models import Inventario

            inventario = Inventario.objects.filter(producto=producto, sucursal=pedido.id_mesa.id_sucursal).first()

            if not inventario or inventario.cantidad < cantidad:
                return Response(
                    {"error": "No hay suficiente stock del producto seleccionado"}, status=status.HTTP_400_BAD_REQUEST
                )
        except Producto.DoesNotExist:
            return Response({"error": "El producto seleccionado no existe"}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el detalle del pedido y actualizar el total
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            detalle = serializer.save()

            # Actualizar el total del pedido
            pedido.total += detalle.subtotal
            pedido.save()

            # Actualizar el inventario
            TransaccionInventario.objects.create(
                id_producto=producto,
                id_sucursal=pedido.id_mesa.id_sucursal,
                cantidad=-cantidad,  # Cantidad negativa porque es una venta
                tipo_transaccion="venta",
                id_usuario=request.user,
                comentario=f"Venta en pedido #{pedido.id_pedido}",
            )

            inventario.cantidad -= cantidad
            inventario.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PedidoMeseroViewSet(viewsets.ModelViewSet):
    queryset = PedidoMesero.objects.all()
    serializer_class = PedidoMeseroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id_pedido", "id_mesero"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]  # Solo admin puede gestionar asignaciones
        else:
            permission_classes = [IsAdminOCajero | IsMesero]  # Todos pueden ver
        return [permission() for permission in permission_classes]


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all().order_by("-fecha_hora")
    serializer_class = PagoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["id_pedido", "id_usuario", "metodo_pago"]
    search_fields = ["referencia_pago"]
    ordering_fields = ["fecha_hora", "monto"]

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [IsAdminOCajero]  # Solo admin y cajero pueden crear pagos
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]  # Solo admin puede modificar/eliminar
        else:
            permission_classes = [IsAdminOCajero]  # Solo admin y cajero pueden ver pagos
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # Asignar el usuario actual como el cajero que registra el pago
        request.data["id_usuario"] = request.user.id_usuario

        # Procesar el pago
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            pago = serializer.save()

            # Actualizar el estado del pedido
            pedido = pago.id_pedido
            pedido.estado = "pagado"
            pedido.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
