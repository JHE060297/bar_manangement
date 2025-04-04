# Generated by Django 5.2 on 2025-04-04 19:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sucursal",
            fields=[
                ("id_sucursal", models.AutoField(primary_key=True, serialize=False)),
                ("nombre_sucursal", models.CharField(max_length=100)),
                ("direccion", models.CharField(max_length=255)),
                ("telefono", models.CharField(max_length=20)),
            ],
            options={
                "verbose_name": "Sucursal",
                "verbose_name_plural": "Sucursales",
                "db_table": "sucursal",
            },
        ),
        migrations.CreateModel(
            name="Mesa",
            fields=[
                ("id_mesa", models.AutoField(primary_key=True, serialize=False)),
                ("numero", models.IntegerField()),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("libre", "Libre"),
                            ("ocupada", "Ocupada"),
                            ("pagado", "Pagado"),
                        ],
                        default="libre",
                        max_length=10,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "id_sucursal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mesas",
                        to="sucursales.sucursal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Mesa",
                "verbose_name_plural": "Mesas",
                "db_table": "mesa",
                "unique_together": {("numero", "id_sucursal")},
            },
        ),
    ]
