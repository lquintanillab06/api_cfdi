# Generated by Django 4.2.9 on 2024-02-23 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administracion_cfdi", "0012_comprobantefiscalimpuesto_tipo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comprobantefiscalconcepto",
            name="descripcion",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
