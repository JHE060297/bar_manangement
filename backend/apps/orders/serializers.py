from rest_framework import serializers
from .models import Order, OrderItem, Payment
from apps.inventory.models import Inventory, InventoryTransaction


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "quantity", "price", "notes", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=False, required=False)
    waiter_name = serializers.CharField(source="waiter.get_full_name", read_only=True)
    table_number = serializers.IntegerField(source="table.number", read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    branch_name = serializers.CharField(source="branch.name", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "table",
            "table_number",
            "waiter",
            "waiter_name",
            "status",
            "notes",
            "created_at",
            "updated_at",
            "prepared_at",
            "delivered_at",
            "paid_at",
            "items",
            "total",
            "branch_name",
        ]
        read_only_fields = ["created_at", "updated_at", "prepared_at", "delivered_at", "paid_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]

            # Verificar disponibilidad en inventario
            inventory = Inventory.objects.get(branch=order.table.branch, product=product)
            if inventory.quantity < quantity:
                raise serializers.ValidationError(f"No hay suficiente stock de {product.name}")

            # Crear item de orden
            OrderItem.objects.create(
                order=order, product=product, quantity=quantity, price=product.price, notes=item_data.get("notes", "")
            )

            # Actualizar inventario
            InventoryTransaction.objects.create(
                inventory=inventory,
                quantity=-quantity,
                transaction_type="sale",
                reference=f"Pedido #{order.id}",
                created_by=validated_data.get("waiter"),
            )

        return order

    def update(self, instance, validated_data):
        # No permitir actualizar items una vez creada la orden
        validated_data.pop("items", None)

        # Si se actualiza el estado, registrar timestamp
        if "status" in validated_data:
            new_status = validated_data["status"]

            if new_status == "preparing" and instance.status != "preparing":
                validated_data["prepared_at"] = None
            elif new_status == "delivered" and instance.status != "delivered":
                validated_data["delivered_at"] = None
            elif new_status == "paid" and instance.status != "paid":
                validated_data["paid_at"] = None

        return super().update(instance, validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    order_total = serializers.DecimalField(source="order.total", max_digits=10, decimal_places=2, read_only=True)
    processed_by_name = serializers.CharField(source="processed_by.get_full_name", read_only=True)
    payment_method_display = serializers.CharField(source="get_payment_method_display", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "order_total",
            "amount",
            "payment_method",
            "payment_method_display",
            "reference_number",
            "payment_date",
            "processed_by",
            "processed_by_name",
            "notes",
        ]
        read_only_fields = ["payment_date"]

    def create(self, validated_data):
        order = validated_data.get("order")

        # Verificar si el pedido ya está pagado
        if order.status == "paid":
            raise serializers.ValidationError("Este pedido ya ha sido pagado")

        # Crear el pago
        payment = Payment.objects.create(**validated_data)

        # Actualizar el estado del pedido
        order.status = "paid"
        order.save()

        return payment
