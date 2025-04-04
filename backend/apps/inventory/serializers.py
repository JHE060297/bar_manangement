from rest_framework import serializers
from .models import Producto, Inventario, TransaccionInventario


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            "id_producto",
            "nombre_producto",
            "descripcion",
            "precio_compra",
            "precio_venta",
            "image",
            "is_active",
        ]


class InventarioSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.CharField(source="producto.nombre_producto", read_only=True)
    nombre_sucursal = serializers.CharField(source="sucursal.nombre_sucursal", read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Inventario
        fields = [
            "id_inventario",
            "producto",
            "nombre_producto",
            "sucursal",
            "nombre_sucursal",
            "cantidad",
            "alert_threshold",
            "is_low_stock",
        ]


class TransaccionInventarioSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.CharField(source="id_producto.nombre_producto", read_only=True)
    nombre_sucursal = serializers.CharField(source="id_sucursal.nombre_sucursal", read_only=True)
    nombre_usuario = serializers.CharField(source="id_usuario.get_full_name", read_only=True)

    class Meta:
        model = TransaccionInventario
        fields = [
            "id_transaccion",
            "id_producto",
            "nombre_producto",
            "id_sucursal",
            "nombre_sucursal",
            "cantidad",
            "tipo_transaccion",
            "transaccion_fecha_hora",
            "id_usuario",
            "nombre_usuario",
            "comentario",
        ]
        read_only_fields = ["transaccion_fecha_hora"]
