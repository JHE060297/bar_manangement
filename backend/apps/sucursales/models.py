from django.db import models


class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    nombre_sucursal = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        db_table = "sucursal"

    def __str__(self):
        return self.nombre_sucursal


class Mesa(models.Model):
    ESTADO_CHOICES = [
        ("libre", "Libre"),
        ("ocupada", "Ocupada"),
        ("pagado", "Pagado"),
    ]

    id_mesa = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default="libre")
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="mesas")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        db_table = "mesa"
        unique_together = ("numero", "id_sucursal")

    def __str__(self):
        status = "🟢" if self.is_active else "🔴"
        return f"{status} {self.id_sucursal.nombre_sucursal} - Mesa {self.numero} ({self.get_estado_display()})"
