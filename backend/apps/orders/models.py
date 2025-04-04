from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import Usuario
from apps.sucursales.models import Mesa


class Pedido(models.Model):
    STATUS_CHOICES = [
        ("pendiente", "Pendiente"),
        ("entregado", "Entregado"),
        ("pagado", "Pagado"),
    ]

    id_pedido = models.AutoField(primary_key=True)
    id_mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name="pedidos")
    estado = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        db_table = "pedido"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Pedido {self.id_pedido} - Mesa {self.id_mesa.numero} - {self.get_estado_display()}"

    def calcular_total(self):
        """Método para calcular el total del pedido a partir de los ítems"""
        # Aquí irá la lógica para calcular el total si tienes un modelo ItemPedido
        # Por ahora, solo retorna el valor actual
        return self.total


class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey("Pedido", on_delete=models.CASCADE, related_name="detalles")
    id_producto = models.ForeignKey("inventory.Producto", on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        verbose_name = "Detalle de Pedido"
        verbose_name_plural = "Detalles de Pedidos"
        db_table = "detalle_pedido"

    def __str__(self):
        return f"{self.id_pedido.id_pedido} - {self.id_producto.nombre_producto} (x{self.cantidad})"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario


class PedidoMesero(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="pedidos_mesero")
    id_mesero = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pedidos_mesero")

    class Meta:
        verbose_name = "Asignación Pedido-Mesero"
        verbose_name_plural = "Asignaciones Pedido-Mesero"
        db_table = "pedido_mesero"
        unique_together = ("id_pedido", "id_mesero")  # Evitar duplicados

    def __str__(self):
        return f"Pedido {self.id_pedido.id_pedido} - Mesero {self.id_mesero.nombre}"


class Pago(models.Model):
    METODOS_PAGO = [
        ("efectivo", "Efectivo"),
        ("tarjeta", "Tarjeta de crédito/débito"),
        ("nequi", "Nequi"),
        ("daviplata", "Daviplata"),
    ]

    id_pago = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="pagos")
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pagos")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=15, choices=METODOS_PAGO)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    # Campos adicionales que podrías necesitar
    referencia_pago = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        db_table = "pago"

    def __str__(self):
        return f"Pago {self.id_pago} - Pedido {self.id_pedido.id_pedido} - {self.monto}"


# Señales para actualizar el estado de la mesa cuando se crea/actualiza un pedido
@receiver(post_save, sender=Pedido)
def update_table_status(sender, instance, created, **kwargs):
    mesa = instance.id_mesa  # Corregido para usar id_mesa

    if created:
        if mesa.estado == "libre":
            mesa.estado = "ocupada"
            mesa.save()
    elif instance.estado == "pagado":
        # No liberamos la mesa inmediatamente, esperamos a que el cajero la marque como libre
        pass

    # La mesa se liberará manualmente por el cajero
