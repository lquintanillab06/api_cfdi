from django.db import models
import uuid
from .managers.contribuyente_manager import ContribuyenteManager



class RegimenFiscal(models.Model):
    clave = models.CharField(max_length=5)
    descripcion = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        managed = True
        db_table = 'regimen_fiscal'

class Contribuyente(models.Model):
    clave  = models.CharField(max_length=15,null=True,blank=True)
    razon_social = models.CharField(max_length=255,blank= True, null=True)
    rfc = models.CharField(max_length=13,blank=True,null=True,unique=True)
    regimen_fiscal = models.ForeignKey(RegimenFiscal,on_delete=models.DO_NOTHING,null=True,blank=True)
    calle = models.CharField(max_length=255,null=True,blank=True)
    codigo_postal = models.CharField(max_length=255,null=True,blank=True)
    colonia = models.CharField(max_length=255, null=True,blank=True)
    estado = models.CharField(max_length=255, null=True,blank=True)
    municipio = models.CharField(max_length=255,null=True,blank=True)
    numero_exterior = models.CharField(max_length=255,null=True,blank=True)
    numero_interior = models.CharField(max_length=255, null=True,blank=True)
    pais = models.CharField(max_length=255, null=True,blank=True)
    numero_certificado = models.CharField(max_length=255,null=True)
    password_pac = models.CharField(max_length=255,blank=True,null=True)
    password_pfx = models.CharField(max_length=255,blank=True,null=True)
    password_key = models.CharField(max_length=255,blank=True,null=True)
    certificado_digital = models.BinaryField(null=True,blank=True)
    certificado_digital_pfx = models.BinaryField(null=True,blank=True)
    llave_privada = models.BinaryField(null=True,blank=True)
    certificado_digital_firma = models.BinaryField(null=True,blank=True)
    llave_privada_firma = models.BinaryField(null=True,blank=True)
    password_key_firma = models.CharField(max_length=255,blank=True,null=True)
    encrypted_key = models.CharField(max_length=255,blank=True,null=True)
    timbrado_de_prueba = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    files_path = models.CharField(max_length=255,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)

    objects = ContribuyenteManager()

    class Meta:
        managed = True
        db_table = 'contribuyente'


class UsoDeCfdi(models.Model):
    
    clave = models.CharField(max_length=5)
    descripcion = models.CharField(max_length=255)
    persona_fisica = models.BooleanField(default=False)
    persona_moral = models.BooleanField(default=False)
    regimen_fiscal = models.ManyToManyField(RegimenFiscal)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        managed = True
        db_table = 'uso_cfdi'

class MetodoPago(models.Model):
    clave = models.CharField(max_length=5)
    descripcion = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        managed = True
        db_table = 'metodo_pago'

class FormaPago(models.Model):
    clave = models.CharField(max_length=5)
    descripcion = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        managed = True
        db_table = 'forma_pago'

class TipoComprobante(models.Model):
    clave = models.CharField(max_length=5)
    descripcion = models.CharField(max_length=255)
    tipo= models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        managed = True
        db_table = 'tipo_comprobante'

class SubTipoComprobante(models.Model):
    clave = models.CharField(max_length=5)
    descripcion = models.CharField(max_length=255)
    tipo= models.CharField(max_length=50, null=True)
    tipo_comprobante = models.ForeignKey(TipoComprobante,on_delete=models.CASCADE,related_name='subtipos')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        managed = True
        db_table = 'subtipo_comprobante'


class ProductoSat(models.Model):
    clave_prod_serv = models.CharField(unique=True, max_length=255)
    descripcion = models.CharField(max_length=255)
    similares = models.CharField(max_length=255,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        managed = True
        db_table = 'producto_sat'

class UnidadSat(models.Model):
    clave_unidad_sat = models.CharField(max_length=255, blank=True, null=True)
    unidad_sat = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255,null=True,blank=True)
    nota = models.CharField(max_length=255,null=True,blank= True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        managed = True
        db_table = 'unidad_sat'


class Cfdi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateTimeField()
    tipo_de_comprobante = models.CharField(max_length=1)
    origen = models.CharField(max_length=255)
    serie = models.CharField(max_length=30, blank=True, null=True)
    folio = models.CharField(max_length=30, blank=True, null=True)
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    total = models.DecimalField(max_digits=19, decimal_places=2)
    emisor_rfc = models.CharField(max_length=13)
    emisor = models.CharField(max_length=255)
    file_name = models.CharField(max_length=150)
    receptor_rfc = models.CharField(max_length=13)
    receptor = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    status = models.CharField(max_length=255, blank=True, null=True)
    cancelado = models.IntegerField(blank=True, null=True)
    cancel_status = models.CharField(max_length=255, blank=True, null=True)
    comentario_cancel = models.CharField(max_length=255, blank=True, null=True)
    status_code = models.CharField(max_length=200, blank=True, null=True)
    is_cancelable = models.CharField(max_length=255, blank=True, null=True)
    enviado = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    version_cfdi = models.CharField(max_length=3)
    uuid_relacionado = models.CharField(max_length=255, blank=True, null=True)
    tipo_de_relacion = models.CharField(max_length=255, blank=True, null=True)
    cadena_original =  models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    

    class Meta:
        managed = True
        db_table = 'cfdi'

class Comprobante(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cfdi = models.ForeignKey(Cfdi,on_delete=models.DO_NOTHING,null=True,blank=True)


    class Meta:
        managed = True
        db_table = 'comprobante'


class ComprobanteConceptos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comprobante = models.ForeignKey(Comprobante,on_delete=models.DO_NOTHING,null=True,blank=True)

    class Meta:
        managed = True
        db_table = 'comprobante_conceptos'


