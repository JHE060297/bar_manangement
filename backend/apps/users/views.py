from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import IsAdmin
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["id_rol", "is_active", "id_sucursal"]
    search_fields = ["email", "nombre", "apellido", "usuario"]
    ordering_fields = ["date_joined", "nombre", "apellido", "id_rol"]

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"status": "usuario activado"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"status": "usuario desactivado"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def change_role(self, request, pk=None):
        user = self.get_object()
        role_id = request.data.get("id_rol")

        if not role_id:
            return Response({"error": "ID del rol no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        from .models import Rol

        try:
            role = Rol.objects.get(id_rol=role_id)
            user.id_rol = role
            user.save()
            return Response({"status": "rol cambiado exitosamente"})
        except Rol.DoesNotExist:
            return Response({"error": "Rol no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["post"])
    def change_branch(self, request, pk=None):
        user = self.get_object()
        sucursal_id = request.data.get("id_sucursal")

        if not sucursal_id:
            return Response({"error": "ID de la sucursal no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        from apps.sucursales.models import Sucursal

        try:
            sucursal = Sucursal.objects.get(id_sucursal=sucursal_id)
            user.id_sucursal = sucursal
            user.save()
            return Response({"status": "sucursal cambiada exitosamente"})
        except Sucursal.DoesNotExist:
            return Response({"error": "Sucursal no encontrada"}, status=status.HTTP_404_NOT_FOUND)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "usuario"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadir datos personalizados al token
        token["nombre"] = user.nombre
        token["apellido"] = user.apellido
        token["rol"] = user.id_rol.nombre
        token["is_admin"] = user.is_admin()

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
