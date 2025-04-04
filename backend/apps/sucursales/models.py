from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return self.name


class Table(models.Model):
    STATUS_CHOICES = [
        ("free", "Libre"),
        ("occupied", "Ocupada"),
        ("reserved", "Reservada"),
        ("dirty", "Sucia"),
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="tables")
    number = models.IntegerField()
    capacity = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="free")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        unique_together = ("branch", "number")

    def __str__(self):
        return f"{self.branch.name} - Mesa {self.number} ({self.get_status_display()})"
