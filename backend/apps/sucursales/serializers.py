from rest_framework import serializers
from .models import Sucursal, Mesa


class SucursalSerializer(serializers.ModelSerializer):
    mesas_count = serializers.SerializerMethodField()

    class Meta:
        model = Sucursal
        fields = ["id_sucursal", "nombre_sucursal", "direccion", "telefono", "mesas_count"]

    def get_mesas_count(self, obj):
        return obj.mesas.count()


class MesasSerializer(serializers.ModelSerializer):
    nombre_sucursal = serializers.CharField(source="id_sucursal.nombre_sucursal", read_only=True)

    class Meta:
        model = Mesa
        fields = ["id_mesa", "id_sucursal", "nombre_sucursal", "numero", "estado", "is_active"]
