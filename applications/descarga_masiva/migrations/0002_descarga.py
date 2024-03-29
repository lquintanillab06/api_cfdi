# Generated by Django 4.2.9 on 2024-01-26 12:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("descarga_masiva", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Descarga",
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
                ("tipo", models.CharField(blank=True, max_length=255, null=True)),
                ("file_name", models.CharField(blank=True, max_length=255, null=True)),
                ("file_url", models.CharField(blank=True, max_length=255, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "solicitud",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="descargas",
                        to="descarga_masiva.solicituddescarga",
                    ),
                ),
            ],
            options={"db_table": "descarga", "managed": True,},
        ),
    ]
