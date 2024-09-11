from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import datetime
from applications.cfdi.models import Contribuyente
from applications.descarga_masiva.models import SolicitudDescarga

from .services import  solicitar_descarga,consultar_solicitud


# Create your views here.
@api_view(['GET'])
def solicitud_descarga_masiva_retenciones(request):
    print("Probando la Descarga Masiva")
    contribuyente_id = request.query_params['contribuyente_id']
    tipo_descarga = request.query_params['tipo_descarga']
    tipo = request.query_params['tipo']
    f_inicial = request.query_params['fecha_inicial']
    f_final = request.query_params['fecha_final']
    contribuyente = Contribuyente.objects.get(pk=contribuyente_id)
    print(contribuyente.clave)
   
    fecha_inicial = datetime.date.fromisoformat(f_inicial)
    fecha_final = datetime.date.fromisoformat(f_final)
    solicitud = solicitar_descarga(contribuyente, tipo_descarga,fecha_inicial, fecha_final,tipo)
    

    return Response({"message":"Hello, world!"})


@api_view(['GET'])
def descarga_masiva_verificacion_retenciones(request):

    contribuyente_id = request.query_params['contribuyente_id']
    contribuyente = Contribuyente.objects.get(pk=contribuyente_id)
    consultar_solicitud(contribuyente)

    return JsonResponse({'message':'La solicitud ya fue verificada'})
