# Generated by Django 4.2.9 on 2024-08-28 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("administracion_cfdi", "0015_comprobantefiscal_cancelado_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="comprobantefiscalconceptoimpuesto",
            name="comprobante_fiscal",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comprobante_fiscal_concepto_impuestos",
                to="administracion_cfdi.comprobantefiscal",
            ),
        ),
        migrations.AlterField(
            model_name="comprobantefiscalimpuesto",
            name="comprobante_fiscal",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comprobante_fiscal_impuestos",
                to="administracion_cfdi.comprobantefiscal",
            ),
        ),
    ]
