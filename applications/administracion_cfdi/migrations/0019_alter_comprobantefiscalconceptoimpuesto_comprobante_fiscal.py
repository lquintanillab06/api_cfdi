# Generated by Django 4.2.9 on 2024-09-03 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administracion_cfdi", "0018_satcomprobanteimpuestos_fecha_timbrado"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comprobantefiscalconceptoimpuesto",
            name="comprobante_fiscal",
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
