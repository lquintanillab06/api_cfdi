# Generated by Django 4.2.9 on 2024-02-13 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ComprobanteFiscal",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("emisor", models.CharField(blank=True, max_length=255, null=True)),
                ("receptor", models.CharField(blank=True, max_length=255, null=True)),
                ("fecha", models.DateField(blank=True, null=True)),
                ("uuid", models.CharField(blank=True, max_length=255, null=True)),
                ("rfc_emisor", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "rfc_receptor",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("serie", models.CharField(blank=True, max_length=255, null=True)),
                ("folio", models.CharField(blank=True, max_length=255, null=True)),
                ("fecha_timbrado", models.DateTimeField(blank=True, null=True)),
                (
                    "regimen_fiscal",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "domicilio_fiscal",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("forma_pago", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "metodo_pago",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("uso_cfdi", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "importe",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "descuento",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "impuesto",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "iva_retenido",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "isr_retenido",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                ("moneda", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "tipo_cambio",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("file_name", models.CharField(blank=True, max_length=255, null=True)),
                ("file_path", models.CharField(blank=True, max_length=255, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={"db_table": "comprobante_fiscal", "managed": True,},
        ),
    ]