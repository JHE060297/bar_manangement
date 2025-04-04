from rest_framework import serializers
from .models import Reporte


class ReporteSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source="usuario.get_full_name", read_only=True)
    sucursal_nombre = serializers.CharField(source="sucursal.nombre_sucursal", read_only=True)

    class Meta:
        model = Reporte
        fields = [
            "id_reporte",
            "usuario",
            "usuario_nombre",
            "sucursal",
            "sucursal_nombre",
            "fecha_generacion",
            "fecha_inicio",
            "fecha_fin",
            "formato",
        ]
        read_only_fields = ["fecha_generacion"]
