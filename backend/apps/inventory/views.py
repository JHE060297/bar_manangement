from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from .models import Producto, Inventario, TransaccionInventario
from .serializers import ProductoSerializer, InventarioSerializer, TransaccionInventarioSerializer
from apps.users.permissions import IsAdmin, IsAdminOCajero, IsMesero


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre_producto", "descripcion"]
    filterset_fields = ["is_active"]
    ordering_fields = ["nombre_producto", "precio_venta"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOCajero | IsMesero]  # Todos pueden ver los productos
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def toggle_active(self, request, pk=None):
        producto = self.get_object()
        producto.is_active = not producto.is_active
        producto.save()
        status_text = "activado" if producto.is_active else "desactivado"
        return Response({"status": f"Producto {status_text} exitosamente"})


class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["sucursal", "producto"]
    search_fields = ["producto__nombre_producto"]
    ordering_fields = ["cantidad"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsAdminOCajero | IsMesero]  # Todos pueden ver el inventario
        else:
            permission_classes = [IsAdminOCajero]  # Solo admin y cajero pueden hacer otras acciones
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def adjust_stock(self, request, pk=None):
        inventario = self.get_object()
        cantidad = request.data.get("cantidad")
        tipo = request.data.get("tipo_transaccion", "ajuste")
        comentario = request.data.get("comentario", "")

        if cantidad is None:
            return Response({"error": "La cantidad es obligatoria"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cantidad = int(cantidad)
        except ValueError:
            return Response({"error": "La cantidad debe ser un número entero"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Crear la transacción
                transaccion = TransaccionInventario.objects.create(
                    id_producto=inventario.producto,
                    id_sucursal=inventario.sucursal,
                    cantidad=cantidad,
                    tipo_transaccion=tipo,
                    id_usuario=request.user,
                    comentario=comentario,
                )

                # Actualizar el inventario
                inventario.cantidad += cantidad
                if inventario.cantidad < 0:
                    return Response(
                        {"error": "La cantidad resultante en inventario no puede ser negativa"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                inventario.save()

                return Response(
                    {"status": "Inventario actualizado exitosamente", "nueva_cantidad": inventario.cantidad}
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TransaccionInventarioViewSet(viewsets.ModelViewSet):
    queryset = TransaccionInventario.objects.all().order_by("-transaccion_fecha_hora")
    serializer_class = TransaccionInventarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["id_sucursal", "id_producto", "tipo_transaccion", "id_usuario"]
    search_fields = ["id_producto__nombre_producto", "comentario"]
    ordering_fields = ["transaccion_fecha_hora", "cantidad"]

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [IsAdminOCajero]  # Solo admin y cajero pueden crear transacciones
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]  # Solo admin puede modificar/eliminar
        else:
            permission_classes = [IsAdminOCajero]  # Solo admin y cajero pueden ver las transacciones
        return [permission() for permission in permission_classes]
