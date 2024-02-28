# Generated by Django 4.2.9 on 2024-02-09 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cfdi", "0006_delete_codigospostalesmx"),
    ]

    operations = [
        migrations.CreateModel(
            name="CodigosPostalesMX",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("estado", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "asentamiento",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("codigo", models.CharField(blank=True, max_length=255, null=True)),
                ("colonia", models.CharField(blank=True, max_length=255, null=True)),
                ("municipio", models.CharField(blank=True, max_length=255, null=True)),
                ("ciudad", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "municipio_sat",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "localidad_sat",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("codigo_sat", models.CharField(blank=True, max_length=255, null=True)),
                ("estado_sat", models.CharField(blank=True, max_length=255, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={"db_table": "codigos_postales_mx", "managed": False,},
        ),
    ]
