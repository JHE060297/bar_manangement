from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Usuario
from .serializers import UserSerializer
from .permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["role", "is_active", "branch"]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["date_joined", "first_name", "last_name", "role"]

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"status": "usuario activado"})

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"status": "usuario desactivado"})

    @action(detail=True, methods=["post"])
    def change_role(self, request, pk=None):
        user = self.get_object()
        role = request.data.get("role")

        if role not in [r[0] for r in User.ROLES]:
            return Response({"error": "Rol inválido"}, status=status.HTTP_400_BAD_REQUEST)

        user.role = role
        user.save()
        return Response({"status": "rol cambiado exitosamente"})
