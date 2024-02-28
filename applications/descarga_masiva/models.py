from django.db import models
import uuid


class SolicitudDescarga(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    solicitud_id = models.CharField(max_length=255, blank=True, null=True)
    rfc = models.CharField(max_length=255, blank=True, null=True)
    razon_social = models.CharField(max_length=255, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    estatus = models.CharField(max_length=255, blank=True, null=True)
    pendiente = models.BooleanField(default=True)
    tipo = models.CharField(max_length=255, blank=True, null=True)
    tipo_solicitud = models.CharField(max_length=255, blank=True, null=True)
    importada = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)


    class Meta:
        managed = True
        db_table = 'solicitud_descarga'


class Descarga(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    solicitud = models.ForeignKey(SolicitudDescarga,on_delete=models.CASCADE,related_name='descargas')
    tipo = models.CharField(max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_url = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)


    class Meta:
        managed = True
        db_table = 'descarga'

class CodigoRespuestaDescarga(models.Model):
    codigo = models.CharField(max_length=255, blank=True, null=True)
    mensaje = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)


    class Meta:
        managed = True
        db_table = 'codigo_respuesta_descarga'
      