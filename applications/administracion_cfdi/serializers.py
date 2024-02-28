from rest_framework import serializers
from .models import ComprobanteFiscal



class ComprobanteFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprobanteFiscal
        fields = '__all__'
        read_only_fields = ('id', 'date_created', 'last_updated')
