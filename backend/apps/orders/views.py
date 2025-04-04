from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer
from apps.users.permissions import IsAdmin, IsAdminOrCashier, IsWaiter


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["table", "waiter", "status", "table__branch"]
    search_fields = ["id", "notes"]
    ordering_fields = ["created_at", "status"]

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [IsWaiter]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsWaiter | IsAdminOrCashier]
        else:
            permission_classes = [IsAdminOrCashier | IsWaiter]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Asignar el mesero actual
        serializer.save(waiter=self.request.user)

    @action(detail=True, methods=["post"])
    def change_status(self, request, pk=None):
        order = self.get_object()
        status = request.data.get("status")

        if status not in [choice[0] for choice in Order.STATUS_CHOICES]:
            return Response({"error": "Estado inválido"}, status=400)

        # Actualizar estado y registro de tiempo
        if status == "preparing" and order.status != "preparing":
            order.prepared_at = timezone.now()
        elif status == "delivered" and order.status != "delivered":
            order.delivered_at = timezone.now()
        elif status == "paid" and order.status != "paid":
            order.paid_at = timezone.now()

        order.status = status
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def active(self, request):
        active_orders = Order.objects.exclude(status__in=["paid", "cancelled"])
        serializer = self.get_serializer(active_orders, many=True)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["order", "product"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsWaiter]
        else:
            permission_classes = [IsAdminOrCashier | IsWaiter]
        return [permission() for permission in permission_classes]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["order", "payment_method", "processed_by"]
    search_fields = ["reference_number", "notes"]
    ordering_fields = ["payment_date", "amount"]

    def get_permissions(self):
        if self.action in ["create", "retrieve", "list"]:
            permission_classes = [IsAdminOrCashier]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Asignar el cajero actual
        serializer.save(processed_by=self.request.user)
