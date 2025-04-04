from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Sucursal, Mesa
from .serializers import SucursalSerializer, MesaSerializer
from apps.users.permissions import IsAdmin, IsAdminOCajero, IsMesero, IsCajero


class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre_sucursal", "direccion"]
    ordering_fields = ["nombre_sucursal"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOCajero | IsMesero]
        return [permission() for permission in permission_classes]


class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["id_sucursal", "estado", "is_active"]
    search_fields = ["numero"]
    ordering_fields = ["numero", "estado"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        elif self.action == "liberar_mesa":
            permission_classes = [IsAdminOCajero]  # Solo admin y cajero pueden liberar mesas
        elif self.action == "cambiar_estado":
            permission_classes = [IsAdminOCajero | IsMesero]  # Ambos pueden cambiar estados
        else:
            permission_classes = [IsAdminOCajero | IsMesero]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def cambiar_estado(self, request, pk=None):
        mesa = self.get_object()
        estado = request.data.get("estado")

        if estado not in [choice[0] for choice in Mesa.ESTADO_CHOICES]:
            return Response({"error": "Estado inválido"}, status=400)

        mesa.estado = estado
        mesa.save()
        return Response({"status": "estado de la mesa actualizado"})

    @action(detail=True, methods=["post"])
    def liberar_mesa(self, request, pk=None):
        mesa = self.get_object()
        mesa.estado = "libre"
        mesa.save()
        return Response({"status": "mesa liberada exitosamente"})
