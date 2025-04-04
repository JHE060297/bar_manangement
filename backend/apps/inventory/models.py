from django.db import models
from apps.sucursales.models import Sucursal
from apps.users.models import Usuario


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = "productos"

    def __str__(self):
        return f"{self.nombre_producto} - ${self.precio_venta}"


class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="existencias")
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="inventarios")
    cantidad = models.IntegerField(default=0)
    alert_threshold = models.IntegerField(default=2)

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        unique_together = ("sucursal", "producto")

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.sucursal.nombre_sucursal}: {self.cantidad} unidades"

    @property
    def is_low_stock(self):
        return self.cantidad <= self.alert_threshold


class TransaccionInventario(models.Model):
    TRANSACTION_TYPES = [
        ("compra", "Compra"),
        ("venta", "Venta"),
        ("ajuste", "Ajuste"),
        ("transferencia", "Transferencia"),
    ]

    id_transaccion = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="transacciones")
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="transacciones")
    cantidad = models.IntegerField()  # Puede ser negativo para salidas
    tipo_transaccion = models.CharField(max_length=13, choices=TRANSACTION_TYPES)
    transaccion_fecha_hora = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Transacción de Inventario"
        verbose_name_plural = "Transacciones de Inventario"
        db_table = "inventario_transaccion"

    def __str__(self):
        return f"{self.get_tipo_transaccion_display()} de {self.cantidad} {self.id_producto.nombre_producto} en {self.id_sucursal.nombre_sucursal}"

    def save(self, *args, **kwargs):
        inventario, _ = Inventario.objects.get_or_create(
            producto=self.id_producto, sucursal=self.id_sucursal, defaults={"cantidad": 0}
        )

        # Actualizar la cantidad del inventario
        nueva_cantidad = inventario.cantidad + self.cantidad
        if nueva_cantidad < 0:
            raise ValueError("La cantidad en inventario no puede ser negativa.")
        inventario.save()
        # Guardar la transacción
        super().save(*args, **kwargs)
