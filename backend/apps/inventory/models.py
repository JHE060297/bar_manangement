from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Inventory(models.Model):
    branch = models.ForeignKey("sucursales.Branch", on_delete=models.CASCADE, related_name="inventories")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventories")
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    alert_threshold = models.PositiveIntegerField(default=5)

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        unique_together = ("branch", "product")

    def __str__(self):
        return f"{self.product.name} - {self.branch.name}: {self.quantity} unidades"

    @property
    def is_low_stock(self):
        return self.quantity <= self.alert_threshold


class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("purchase", "Compra"),
        ("sale", "Venta"),
        ("adjustment", "Ajuste"),
        ("transfer", "Transferencia"),
    ]

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="transactions")
    quantity = models.IntegerField()  # Puede ser negativo para salidas
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100, blank=True, null=True)  # Para referencias a órdenes, facturas, etc.
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, related_name="inventory_transactions"
    )

    class Meta:
        verbose_name = "Transacción de Inventario"
        verbose_name_plural = "Transacciones de Inventario"

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.inventory.product.name}: {self.quantity}"

    def save(self, *args, **kwargs):
        # Actualizar la cantidad en el inventario
        self.inventory.quantity += self.quantity
        self.inventory.save()
        super().save(*args, **kwargs)
