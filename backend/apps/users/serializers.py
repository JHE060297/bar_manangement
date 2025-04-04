from rest_framework import serializers
from .models import Usuario, Rol


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ["id_rol", "nombre"]


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    rol_nombre = serializers.CharField(source="id_rol.nombre", read_only=True)
    sucursal_nombre = serializers.CharField(source="id_sucursal.nombre_sucursal", read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id_usuario",
            "nombre",
            "apellido",
            "usuario",
            "password",
            "id_rol",
            "rol_nombre",
            "id_sucursal",
            "sucursal_nombre",
            "is_active",
            "is_staff",
            "date_joined",
        ]
        read_only_fields = ["date_joined"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        usuario = Usuario(**validated_data)
        if password:
            usuario.set_password(password)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super().update(instance, validated_data)
