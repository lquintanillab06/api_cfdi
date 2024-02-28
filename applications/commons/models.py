from django.db import models
import uuid

# Create your models here.
class CodigosPostalesMX(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estado = models.CharField(max_length=255, blank=True, null=True)
    asentamiento = models.CharField(max_length=255, blank=True, null=True)
    codigo = models.CharField(max_length=255, blank=True, null=True)
    colonia = models.CharField(max_length=255, blank=True, null=True)
    municipio = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=255, blank=True, null=True)
    municipio_sat = models.CharField(max_length=255, blank=True, null=True)
    localidad_sat = models.CharField(max_length=255, blank=True, null=True)
    codigo_sat = models.CharField(max_length=255, blank=True, null=True)
    estado_sat = models.CharField(max_length=255, blank=True, null=True)
    pais = models.CharField(max_length=255, blank=True, null=True)
    #date_created = models.DateTimeField(auto_now_add=True, null=True)
    #last_updated = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        managed = True
        db_table = 'codigos_postales_mx'