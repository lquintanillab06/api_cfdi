from rest_framework import serializers
from ..models import CodigoRespuestaDescarga,SolicitudDescarga, Descarga




class CodigoRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoRespuestaDescarga
        fields = '__all__'

class SolicitudDescargaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudDescarga
        fields = '__all__'

class DescargaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descarga
        fields = '__all__'
