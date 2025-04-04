from django.db import models
from apps.users.models import Usuario
from apps.sucursales.models import Sucursal


# Create your models here.
class Reporte(models.Model):

    FORMATOS = [
        ("xlsx", "Excel"),
        ("csv", "CSV"),
        ("pdf", "PDF"),
    ]

    id_reporte = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    formato = models.CharField(max_length=10, choices=FORMATOS)

    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"
        db_table = "reporte"

    def __str__(self):
        return f"Reporte {self.id_reporte} - {self.usuario.usuario} - {self.fecha_generacion}"
