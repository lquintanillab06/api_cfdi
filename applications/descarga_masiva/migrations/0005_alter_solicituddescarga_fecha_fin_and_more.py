# Generated by Django 4.2.9 on 2024-02-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("descarga_masiva", "0004_codigorespuestadescarga"),
    ]

    operations = [
        migrations.AlterField(
            model_name="solicituddescarga",
            name="fecha_fin",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="solicituddescarga",
            name="fecha_inicio",
            field=models.DateField(blank=True, null=True),
        ),
    ]
