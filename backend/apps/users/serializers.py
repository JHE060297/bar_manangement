from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    rol_nombre = serializers.CharField(source="id_rol.nombre_rol", read_only=True)
    sucursal_nombre = serializers.IntegerField(source="id_sucursal.nombre_sucursal", write_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id_usuario",
            "nombre",
            "apellido",
            "usuario",
            "email",
            "id_rol",
            "rol_nombre",
            "id_sucursal",
            "sucursal_nombre",
            "contrasena",
            "is_active",
            "is_staff",
            "date_joined",
        ]
        read_only_fields = ["date_joined"]

    def create(self, validated_data):
        contrasena = validated_data.pop("contrasena", None)
        usuario = Usuario(**validated_data)
        if contrasena:
            usuario.set_password(contrasena)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        if "contrasena" in validated_data:
            contrasena = validated_data.pop("contrasena")
            instance.set_password(contrasena)
        return super().update(instance, validated_data)
