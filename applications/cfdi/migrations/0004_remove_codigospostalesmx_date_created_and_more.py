# Generated by Django 4.2.9 on 2024-02-09 11:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("cfdi", "0003_contribuyente_activo"),
    ]

    operations = [
        migrations.RemoveField(model_name="codigospostalesmx", name="date_created",),
        migrations.RemoveField(model_name="codigospostalesmx", name="last_updated",),
        migrations.AddField(
            model_name="codigospostalesmx",
            name="colonia_sat",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="codigospostalesmx",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
