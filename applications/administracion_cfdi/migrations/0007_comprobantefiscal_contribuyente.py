# Generated by Django 4.2.9 on 2024-02-19 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cfdi", "0010_contribuyente_files_path"),
        ("administracion_cfdi", "0006_alter_comprobantefiscal_fecha"),
    ]

    operations = [
        migrations.AddField(
            model_name="comprobantefiscal",
            name="contribuyente",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="cfdi.contribuyente",
            ),
        ),
    ]
