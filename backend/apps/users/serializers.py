from rest_framework import serializers
from .models import Usuario


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    sucursal_name = serializers.CharField(source="sucursales.name", read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id_usuario",
            "nombre",
            "apellido",
            "usuario",
            "id_rol",
            "contrasena",
            "email",
            "is_active",
            "is_staff",
            "date_joined",
        ]
        read_only_fields = ["date_joined"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super().update(instance, validated_data)
