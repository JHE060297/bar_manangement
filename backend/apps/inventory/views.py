from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Category, Product, Inventory, InventoryTransaction
from .serializers import CategorySerializer, ProductSerializer, InventorySerializer, InventoryTransactionSerializer
from apps.users.permissions import IsAdmin, IsAdminOrCashier, IsWaiter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOrCashier | IsWaiter]
        return [permission() for permission in permission_classes]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOrCashier | IsWaiter]
        return [permission() for permission in permission_classes]


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["branch", "product"]
    search_fields = ["product__name"]
    ordering_fields = ["quantity", "last_updated"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOrCashier | IsWaiter]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        low_stock = Inventory.objects.filter(quantity__lte=models.F("alert_threshold"))
        serializer = self.get_serializer(low_stock, many=True)
        return Response(serializer.data)


class InventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["inventory__branch", "inventory__product", "transaction_type", "created_by"]
    search_fields = ["inventory__product__name", "reference", "notes"]
    ordering_fields = ["transaction_date", "quantity"]

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [IsAdminOrCashier]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsAdminOrCashier | IsWaiter]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Asignar el usuario actual como creador
        serializer.save(created_by=self.request.user)
