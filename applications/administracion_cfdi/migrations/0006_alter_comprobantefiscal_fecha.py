# Generated by Django 4.2.9 on 2024-02-19 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "administracion_cfdi",
            "0005_rename_tipo_de_compribante_comprobantefiscal_tipo_de_comprobante",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="comprobantefiscal",
            name="fecha",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
