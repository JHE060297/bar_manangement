# Generated by Django 5.2 on 2025-04-04 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sucursales", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reporte",
            fields=[
                ("id_reporte", models.AutoField(primary_key=True, serialize=False)),
                ("fecha_generacion", models.DateTimeField(auto_now_add=True)),
                ("fecha_inicio", models.DateField()),
                ("fecha_fin", models.DateField()),
                (
                    "formato",
                    models.CharField(
                        choices=[("xlsx", "Excel"), ("csv", "CSV"), ("pdf", "PDF")],
                        max_length=10,
                    ),
                ),
                (
                    "sucursal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sucursales.sucursal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Reporte",
                "verbose_name_plural": "Reportes",
                "db_table": "reporte",
            },
        ),
    ]
