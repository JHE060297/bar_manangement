from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("preparing", "En preparación"),
        ("ready", "Listo para entregar"),
        ("delivered", "Entregado"),
        ("paid", "Pagado"),
        ("cancelled", "Cancelado"),
    ]

    table = models.ForeignKey("sucursales.Table", on_delete=models.CASCADE, related_name="orders")
    waiter = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name="orders_taken")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Para el seguimiento de tiempos
    prepared_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.table.number} - {self.get_status_display()}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def branch(self):
        return self.table.branch


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio al momento de la orden
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Items de Pedido"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.price * self.quantity


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Efectivo"),
        ("card", "Tarjeta de crédito/débito"),
        ("digital_wallet", "Billetera digital"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHODS)
    reference_number = models.CharField(max_length=100, blank=True, null=True)  # Para referencias de transacciones
    payment_date = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, related_name="payments_processed"
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"Pago {self.id} - Pedido {self.order.id} - {self.amount}"


# Señales para actualizar el estado de la mesa cuando se crea/actualiza un pedido
@receiver(post_save, sender=Order)
def update_table_status(sender, instance, created, **kwargs):
    table = instance.table

    if created:
        if table.status == "free":
            table.status = "occupied"
            table.save()
    elif instance.status == "paid":
        # No liberamos la mesa inmediatamente, esperamos a que el cajero la marque como libre
        pass

    # La mesa se liberará manualmente por el cajero
