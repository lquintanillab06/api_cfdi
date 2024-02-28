from rest_framework.serializers import ModelSerializer
from .models import CodigosPostalesMX


class CodigosPostalesSerializer(ModelSerializer):
    class Meta:
        model = CodigosPostalesMX
        fields = '__all__'
