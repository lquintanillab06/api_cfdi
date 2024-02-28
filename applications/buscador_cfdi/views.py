from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from applications.administracion_cfdi.models import ComprobanteFiscal
from applications.administracion_cfdi.serializers import ComprobanteFiscalSerializer


# Create your views here.
@api_view(['GET'])
def buscador_cfdi(request):
    UUID = request.query_params.get('UUID')
    rfc_receptor = request.query_params.get('rfc_receptor')
    rfc_emisor = request.query_params.get('rfc_emisor')
    fecha_inicial = request.query_params.get('fecha_inicial')
    fecha_final = request.query_params.get('fecha_final')
    print(request.query_params)
    comprobantes = []

    if not UUID  == '':
        try:
            comprobantes = ComprobanteFiscal.objects.filter(uuid=UUID)
            comprobantes_serialized = ComprobanteFiscalSerializer(comprobantes, many=True)
            return Response(comprobantes_serialized.data)
        except ComprobanteFiscal.DoesNotExist:
            pass
            

    if not rfc_receptor == '':
        try:
            comprobantes = ComprobanteFiscal.objects.filter(rfc_receptor=rfc_receptor, fecha__date__range=[fecha_inicial, fecha_final])
            comprobantes_serialized = ComprobanteFiscalSerializer(comprobantes, many=True)
            return Response(comprobantes_serialized.data)
        except ComprobanteFiscal.DoesNotExist:
            pass
    
    if not rfc_emisor == '':
        try:
            comprobantes = ComprobanteFiscal.objects.filter(rfc_emisor=rfc_emisor, fecha__date__range=[fecha_inicial, fecha_final])
            comprobantes_serialized = ComprobanteFiscalSerializer(comprobantes, many=True)
            return Response(comprobantes_serialized.data)
        except ComprobanteFiscal.DoesNotExist:
            pass

    return Response([])