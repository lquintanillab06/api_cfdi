# Generated by Django 4.2.9 on 2024-02-19 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cfdi", "0009_delete_codigospostalesmx"),
    ]

    operations = [
        migrations.AddField(
            model_name="contribuyente",
            name="files_path",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
