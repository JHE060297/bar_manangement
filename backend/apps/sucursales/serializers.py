from rest_framework import serializers
from .models import Sucursal, Mesa


class SucursalSerializer(serializers.ModelSerializer):
    mesas_count = serializers.SerializerMethodField()

    class Meta:
        model = Sucursal
        fields = ["id_sucursal", "nombre_sucursal", "direccion", "telefono", "mesas_count"]

    def get_mesas_count(self, obj):
        return obj.mesas.count()


class MesaSerializer(serializers.ModelSerializer):
    nombre_sucursal = serializers.CharField(source="id_sucursal.nombre_sucursal", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Mesa
        fields = ["id_mesa", "numero", "id_sucursal", "nombre_sucursal", "estado", "estado_display", "is_active"]
