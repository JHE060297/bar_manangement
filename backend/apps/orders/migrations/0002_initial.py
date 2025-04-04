# Generated by Django 5.2 on 2025-04-04 19:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("orders", "0001_initial"),
        ("sucursales", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="pago",
            name="id_usuario",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pagos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="pedido",
            name="id_mesa",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pedidos",
                to="sucursales.mesa",
            ),
        ),
        migrations.AddField(
            model_name="pago",
            name="id_pedido",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pagos",
                to="orders.pedido",
            ),
        ),
        migrations.AddField(
            model_name="detallepedido",
            name="id_pedido",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="detalles",
                to="orders.pedido",
            ),
        ),
        migrations.AddField(
            model_name="pedidomesero",
            name="id_mesero",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pedidos_mesero",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="pedidomesero",
            name="id_pedido",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pedidos_mesero",
                to="orders.pedido",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="pedidomesero",
            unique_together={("id_pedido", "id_mesero")},
        ),
    ]
