# Generated by Django 4.2.9 on 2024-09-12 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administracion_cfdi", "0025_satcomprobanteimpuestos_tipo_de_cambio_pago"),
    ]

    operations = [
        migrations.AddField(
            model_name="satcomprobanteimpuestos",
            name="base_excenta",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0.0, max_digits=10, null=True
            ),
        ),
    ]
