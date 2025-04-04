from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Branch, Table
from .serializers import BranchSerializer, TableSerializer
from apps.users.permissions import IsAdmin, IsAdminOrCashier, IsWaiter


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["name", "address"]
    ordering_fields = ["name", "created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOrCashier | IsWaiter]
        return [permission() for permission in permission_classes]


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["branch", "status", "is_active"]
    search_fields = ["number"]
    ordering_fields = ["number", "capacity", "status"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        elif self.action in ["change_status", "free_table"]:
            permission_classes = [IsAdminOrCashier | IsWaiter]
        else:
            permission_classes = [IsAdminOrCashier | IsWaiter]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def change_status(self, request, pk=None):
        table = self.get_object()
        status = request.data.get("status")

        if status not in [choice[0] for choice in Table.STATUS_CHOICES]:
            return Response({"error": "Estado inválido"}, status=400)

        table.status = status
        table.save()
        return Response({"status": "estado de la mesa actualizado"})

    @action(detail=True, methods=["post"])
    def free_table(self, request, pk=None):
        table = self.get_object()
        table.status = "free"
        table.save()
        return Response({"status": "mesa liberada exitosamente"})
