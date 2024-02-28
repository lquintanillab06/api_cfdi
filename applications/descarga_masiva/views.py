from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.generics import (RetrieveAPIView, ListAPIView,CreateAPIView,DestroyAPIView,UpdateAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView)
from applications.cfdi.models import Contribuyente
from .models import SolicitudDescarga, Descarga, CodigoRespuestaDescarga
from .serializers.solicittud_serializer import CodigoRespuestaSerializer, SolicitudDescargaSerializer, DescargaSerializer
from .services import  solicitar_descarga, consultar_solicitud, solicitar_descarga_uuid
from .utils.utils import file_iterator
import datetime
import os



@api_view(['GET'])
def solicitud_descarga_masiva(request):
    print("Probando la Descarga Masiva")
    contribuyente_id = request.query_params['contribuyente_id']
    tipo_descarga = request.query_params['tipo_descarga']
    tipo = request.query_params['tipo']
    f_inicial = request.query_params['fecha_inicial']
    f_final = request.query_params['fecha_final']
    contribuyente = Contribuyente.objects.get(pk=contribuyente_id)
    print(contribuyente.clave)
    #token = autenticacion(contribuyente)
    fecha_inicial = datetime.date.fromisoformat(f_inicial)
    fecha_final = datetime.date.fromisoformat(f_final)
    solicitud = solicitar_descarga(contribuyente, tipo_descarga,fecha_inicial, fecha_final,tipo)
    if solicitud:
        sol = SolicitudDescarga()
        sol.solicitud_id = solicitud['id_solicitud']
        sol.rfc = contribuyente.rfc
        sol.razon_social = contribuyente.razon_social
        sol.fecha_inicio = fecha_inicial
        sol.fecha_fin = fecha_final
        sol.estatus = solicitud['cod_estatus']
        sol.tipo_solicitud = tipo_descarga
        sol.tipo = tipo
        if not solicitud['cod_estatus'] == '5000':
            sol.pendiente = False
        sol.save() 

        print(sol)
 
        serializer = SolicitudDescargaSerializer(sol)
        return Response(serializer.data)
    return JsonResponse({'message':'Descarga Masiva'})

@api_view(['GET'])
def descarga_masiva_verificacion(request):

    contribuyente_id = request.query_params['contribuyente_id']
    solicitud_id = request.query_params['solicitud_id']
    contribuyente = Contribuyente.objects.get(pk=contribuyente_id)
    solicitud= SolicitudDescarga.objects.get(pk=solicitud_id)

    if solicitud.pendiente:

        estado, pendiente, descargas = consultar_solicitud(contribuyente, solicitud)
        solicitud.estatus = estado
        solicitud.pendiente = pendiente
        solicitud.save()

        if len(descargas) > 0:

            for descarga in descargas:

                descarga_bd = solicitud.descargas.create(tipo=solicitud.tipo_solicitud,file_name=descarga['file_name'],file_url=descarga['file_url'])
                descarga_bd.save()

        return JsonResponse({'message':'Descarga Masiva Verificacion'})
    
    else:

        return JsonResponse({'message':'La solicitud ya fue verificada'})


@api_view(['GET'])
def get_descarga_solicitud(request):
    solicitud_id = request.query_params['solicitud_id']
    solicitud = Descarga.objects.filter(solicitud_id=solicitud_id)
    serializer = DescargaSerializer(solicitud, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def descargar_archivo(request):
    print("Descargando Archivo")
    descarga_id = request.query_params['descarga_id']
    descarga = Descarga.objects.get(pk=descarga_id)
    response = StreamingHttpResponse(file_iterator(descarga.file_url), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(descarga.file_url)}'
    response['Content-Type'] = 'application/zip'
    #return JsonResponse({'message':'Descarga Masiva'})
    return response



class SolicitudesPorContribuyente(ListAPIView):
    serializer_class = SolicitudDescargaSerializer

    def get_queryset(self):
        contribuyente_id = self.request.query_params['contribuyente_id']
        fecha_inicial = self.request.query_params['fecha_inicial']
        fecha_final = self.request.query_params['fecha_final']
        contribuyente = Contribuyente.objects.get(pk=contribuyente_id)
        solicitudes = SolicitudDescarga.objects.filter(rfc=contribuyente.rfc,date_created__date__range=[fecha_inicial, fecha_final]).order_by('-date_created')
        return solicitudes


class CodigoRespuestaViewset(viewsets.ViewSet):

    def list(self, request):
        queryset = CodigoRespuestaDescarga.objects.all()
        serializer = CodigoRespuestaSerializer(queryset,many= True)
        return Response(serializer.data)
    
    def create(self, request):
        print(request)
        return Response("Succesfully Create")
    
    def retrieve(self, request, pk=None):
        queryset = CodigoRespuestaDescarga.objects.filter(pk=pk).first()
        print(queryset)
        serializer = CodigoRespuestaSerializer(queryset)
        return Response(serializer.data)
        
    def update(self, request, pk=None):
        print(request)
        return Response("Succesfully Update")

    def partial_update(self, request, pk=None):
        print(request)
        return Response("Succesfully Partial")

    def destroy(self, request, pk=None):
        print(request)
        return Response("Succesfully")