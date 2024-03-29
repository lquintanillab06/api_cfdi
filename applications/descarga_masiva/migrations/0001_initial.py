# Generated by Django 4.2.9 on 2024-01-25 11:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SolicitudDescarga",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "solicitud_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("rfc", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "razon_social",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("fecha_inicio", models.DateTimeField(blank=True, null=True)),
                ("fecha_fin", models.DateTimeField(blank=True, null=True)),
                ("estatus", models.CharField(blank=True, max_length=255, null=True)),
                ("pendiente", models.BooleanField(default=True)),
                ("tipo", models.CharField(blank=True, max_length=255, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={"db_table": "solicitud_descarga", "managed": True,},
        ),
    ]
