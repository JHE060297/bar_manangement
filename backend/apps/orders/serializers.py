from rest_framework import serializers
from .models import Pedido, DetallePedido, PedidoMesero, Pago
from apps.inventory.serializers import ProductoSerializer


class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="id_producto.nombre_producto", read_only=True)
    producto_precio = serializers.DecimalField(
        source="id_producto.precio_venta", read_only=True, max_digits=10, decimal_places=2
    )
    subtotal = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = DetallePedido
        fields = [
            "id_detalle_pedido",
            "id_pedido",
            "id_producto",
            "producto_nombre",
            "producto_precio",
            "cantidad",
            "precio_unitario",
            "subtotal",
            "descripcion",
        ]
        read_only_fields = ["precio_unitario", "subtotal"]

    def create(self, validated_data):
        # Obtener el precio actual del producto
        producto = validated_data["id_producto"]
        validated_data["precio_unitario"] = producto.precio_venta

        return super().create(validated_data)


class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    mesa_numero = serializers.IntegerField(source="id_mesa.numero", read_only=True)
    sucursal_nombre = serializers.CharField(source="id_mesa.id_sucursal.nombre_sucursal", read_only=True)

    class Meta:
        model = Pedido
        fields = [
            "id_pedido",
            "id_mesa",
            "mesa_numero",
            "sucursal_nombre",
            "estado",
            "total",
            "detalles",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["total", "created_at", "updated_at"]


class PedidoMeseroSerializer(serializers.ModelSerializer):
    nombre_mesero = serializers.CharField(source="id_mesero.get_full_name", read_only=True)

    class Meta:
        model = PedidoMesero
        fields = ["id", "id_pedido", "id_mesero", "nombre_mesero"]


class PagoSerializer(serializers.ModelSerializer):
    nombre_cajero = serializers.CharField(source="id_usuario.get_full_name", read_only=True)
    pedido_detalle = PedidoSerializer(source="id_pedido", read_only=True)

    class Meta:
        model = Pago
        fields = [
            "id_pago",
            "id_pedido",
            "pedido_detalle",
            "id_usuario",
            "nombre_cajero",
            "monto",
            "metodo_pago",
            "fecha_hora",
            "referencia_pago",
        ]
        read_only_fields = ["fecha_hora"]

    def validate(self, data):
        # Verificar que el monto del pago coincida con el total del pedido
        pedido = data["id_pedido"]
        if data["monto"] != pedido.total:
            raise serializers.ValidationError(
                {"monto": f'El monto del pago ({data["monto"]}) no coincide con el total del pedido ({pedido.total})'}
            )

        # Verificar que el pedido no esté ya pagado
        if pedido.estado == "pagado":
            raise serializers.ValidationError("Este pedido ya ha sido pagado")

        return data
