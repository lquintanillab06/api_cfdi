from django.db import models
from applications.cfdi.models import Contribuyente
from .managers import ComprobanteFiscalManager

# Create your models here.


class ComprobanteFiscal(models.Model):
    id = models.AutoField(primary_key=True)
    emisor = models.CharField(max_length=255, blank=True, null=True)
    receptor = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=255, blank=True, null=True,unique=True)
    rfc_emisor = models.CharField(max_length=255, blank=True, null=True)
    rfc_receptor = models.CharField(max_length=255, blank=True, null=True)
    serie = models.CharField(max_length=255, blank=True, null=True)
    folio = models.CharField(max_length=255, blank=True, null=True)
    fecha_timbrado = models.DateTimeField(blank=True, null=True)
    regimen_fiscal = models.CharField(max_length=255, blank=True, null=True)
    regimen_fiscal_receptor = models.CharField(max_length=255, blank=True, null=True)
    domicilio_fiscal = models.CharField(max_length=255, blank=True, null=True)
    forma_pago = models.CharField(max_length=255, blank=True, null=True)
    metodo_pago = models.CharField(max_length=255, blank=True, null=True)
    uso_cfdi = models.CharField(max_length=255, blank=True, null=True)
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    iva_retenido = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    isr_retenido = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    total_impuestos_trasladados = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    total_impuestos_retenidos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    moneda = models.CharField(max_length=255, blank=True, null=True)
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_de_comprobante = models.CharField(max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    contribuyente = models.ForeignKey(Contribuyente,blank=True, null=True, on_delete=models.CASCADE)
    cancelado = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)   

    objects =ComprobanteFiscalManager()

    class Meta:
        managed = True
        db_table = 'comprobante_fiscal'

class ComprobanteFiscalCancelado(models.Model):
    id = models.AutoField(primary_key=True)
    comprobante_fiscal = models.ForeignKey(ComprobanteFiscal, on_delete=models.CASCADE, related_name='comprobante_fiscal_cancelado')
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
    rfc_receptor = models.CharField(max_length=255, blank=True, null=True)
    nombre_receptor = models.CharField(max_length=255, blank=True, null=True)
    rfc_emisor = models.CharField(max_length=255, blank=True, null=True)
    nombre_emisor = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.CharField(max_length=255, blank=True, null=True)
    cancelado = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)  


    class Meta:
        managed = True
        db_table = 'comprobante_fiscal_cancelado'

class ComprobanteFiscalConcepto(models.Model):
    id = models.AutoField(primary_key=True)
    comprobante_fiscal = models.ForeignKey(ComprobanteFiscal, on_delete=models.CASCADE)
    clave_prod_serv = models.CharField(max_length=255, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    clave_unidad = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    objeto_impuesto = models.CharField(max_length=255, blank=True, null=True)
    no_identificacion = models.CharField(max_length=255, blank=True, null=True)
    unidad = models.CharField(max_length=255, blank=True, null=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True) 

    class Meta:
        managed = True
        db_table = 'comprobante_fiscal_concepto'

class ComprobanteFiscalImpuesto(models.Model):
    id = models.AutoField(primary_key=True)
    comprobante_fiscal = models.ForeignKey(ComprobanteFiscal, on_delete=models.CASCADE, related_name='comprobante_fiscal_impuestos')
    base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    tipo_factor = models.CharField(max_length=255, blank=True, null=True)
    tasa_cuota = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    tipo = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)  


    class Meta:
        managed = True
        db_table = 'comprobante_fiscal_impuesto'

class ComprobanteFiscalConceptoImpuesto(models.Model):
    id = models.AutoField(primary_key=True)
    comprobante_fiscal = models.ForeignKey(ComprobanteFiscal, on_delete=models.CASCADE, blank=True, null=True, related_name='comprobante_fiscal_concepto_impuestos')
    comprobante_fiscal_concepto = models.ForeignKey(ComprobanteFiscalConcepto, on_delete=models.CASCADE)
    base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    tipo_factor = models.CharField(max_length=255, blank=True, null=True)
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    tasa_cuota = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    tipo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comprobante_fiscal_concepto_impuesto'

class SatComprobanteImpuestos(models.Model):
    id = models.AutoField(primary_key=True)
    comprobante = models.BigIntegerField(blank=True, null=True)
    receptor = models.CharField(max_length=255, blank=True, null=True)
    rfc_receptor = models.CharField(max_length=255, blank=True, null=True)
    emisor = models.CharField(max_length=255, blank=True, null=True)
    rfc_emisor = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    fecha_timbrado = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=255, blank=True, null=True, unique=True)
    serie = models.CharField(max_length=255, blank=True, null=True)
    folio = models.CharField(max_length=255, blank=True, null=True)
    forma_pago = models.CharField(max_length=255, blank=True, null=True)
    metodo_pago = models.CharField(max_length=255, blank=True, null=True)
    uso_cfdi = models.CharField(max_length=255, blank=True, null=True)
    moneda = models.CharField(max_length=255, blank=True, null=True)
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    tipo_comprobante = models.CharField(max_length=255, blank=True, null=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    iva_trasladado_porc = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True, default=0.00)
    iva_trasladado_importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    iva_retenido_porc = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True, default=0.00)
    iva_retenido_importe = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True, default=0.00)
    isr_retenido_porc = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True, default=0.00)
    isr_retenido_importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    cancelado = models.BooleanField(default=False)
    total_impuestos_trasladados = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    total_impuestos_retenidos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    aclaracion_referencia = models.CharField(max_length=255, blank=True, null=True)
    referencia_pago = models.CharField(max_length=255, blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    forma_de_pago = models.CharField(max_length=255, blank=True, null=True)
    sucursal = models.CharField(max_length=255, blank=True, null=True)
    tipo_documento = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)  

    class Meta:
        managed = True
        db_table = 'sat_comprobante_impuestos'
       