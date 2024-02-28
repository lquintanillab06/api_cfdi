from rest_framework import serializers
from ..models import Contribuyente,UsoDeCfdi,FormaPago,MetodoPago,TipoComprobante,RegimenFiscal,ProductoSat,UnidadSat,SubTipoComprobante

class ContribuyenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribuyente
        fields = '__all__'

class RegimenFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegimenFiscal
        fields = '__all__'

class ContribuyenteShowSerializer(serializers.ModelSerializer):
    regimen_fiscal = RegimenFiscalSerializer()
    class Meta:
        model = Contribuyente
        exclude = ('llave_privada','certificado_digital','certificado_digital_pfx','numero_certificado','password_pac','password_pfx','password_key',
                   'certificado_digital_firma', 'llave_privada_firma','password_key_firma','encrypted_key','timbrado_de_prueba')
        
class ContribuyenteFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribuyente
        fields = ['clave','rfc','razon_social','regimen_fiscal', 'calle', 'numero_exterior', 'numero_interior', 'colonia', 'municipio', 'estado', 'pais', 'codigo_postal']

class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = '__all__'

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'

class TipoComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoComprobante
        fields = '__all__'

    
class SubTipoComprobanteSerializer(serializers.ModelSerializer):
    tipo_comprobante = TipoComprobanteSerializer()
    class Meta:
        model = SubTipoComprobante  
        fields ='__all__'

class SubTipoComprobanteFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTipoComprobante
        fields = '__all__'




class UsoDeCfdiSerializer(serializers.ModelSerializer):
    regimen_fiscal = RegimenFiscalSerializer(many= True)
    class Meta:
        model = UsoDeCfdi
        fields = (
            'id',
            'clave',
            'descripcion',
            'persona_fisica',
            'persona_moral',
            'regimen_fiscal',
            )

class UsoDeCfdiFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsoDeCfdi
        fields = '__all__'


class UsoDeCfdLinkSerializer(serializers.ModelSerializer):
    #regimen_fiscal = RegimenFiscalSerializer(many= True)
    clave_descripcion = serializers.SerializerMethodField()
    regimen_fiscal = serializers.HyperlinkedRelatedField(view_name='regimen_fiscal_retrieve' , lookup_field='pk', many=True, read_only = True)
    class Meta:
        model = UsoDeCfdi
        fields = (
            'id',
            'clave',
            'descripcion',
            'persona_fisica',
            'persona_moral',
            'regimen_fiscal',
            'clave_descripcion',
            )

    def get_clave_descripcion(self,obj):
        return obj.clave + " - " + obj.descripcion
    
class ProductoSatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoSat
        fields = '__all__'
        read_only_fields = ['date_created','last_updated']

class UnidadSatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadSat
        fields = '__all__'