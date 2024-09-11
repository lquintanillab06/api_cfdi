# Generated by Django 4.2.9 on 2024-09-03 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "administracion_cfdi",
            "0020_alter_comprobantefiscalconceptoimpuesto_comprobante_fiscal_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="satcomprobanteimpuestos",
            old_name="isr_retencion_importe",
            new_name="isr_retenido_importe",
        ),
        migrations.RenameField(
            model_name="satcomprobanteimpuestos",
            old_name="isr_retencion_porc",
            new_name="isr_retenido_porc",
        ),
        migrations.RenameField(
            model_name="satcomprobanteimpuestos",
            old_name="tipo_de_comprobante",
            new_name="tipo_comprobante",
        ),
        migrations.AddField(
            model_name="satcomprobanteimpuestos",
            name="cancelado",
            field=models.BooleanField(default=False),
        ),
    ]
