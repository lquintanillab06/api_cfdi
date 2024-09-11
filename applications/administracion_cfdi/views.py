from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.http import StreamingHttpResponse
from .services.services import salvar_xmls_from_zip_file, validar_cancelados
from .services.print_services2 import print_pdf, print_acuse
from .services.comprobante_impuesto_service import make_comprobante_impuestos, get_referencias
from applications.descarga_masiva.services.service import validar_cfdi
from applications.commons.utils.utils_file import file_iterator
import os   
from applications.descarga_masiva.models import Descarga, SolicitudDescarga 
from applications.cfdi.models import Contribuyente
from .models import ComprobanteFiscal, SatComprobanteImpuestos
from .serializers import ComprobanteFiscalSerializer, SatComprobanteImpuestosSerializer
import pandas as pd


# Create your views here.


@api_view(['GET'])
def cargar_xmls_solicitud(request):

    solicitud = request.query_params.get('solicitud_id')
    print(solicitud)
    solicitud_descarga = SolicitudDescarga.objects.get(id=solicitud)
    contribuyente = Contribuyente.objects.get(rfc=solicitud_descarga.rfc)
    comprobantes_importados = []
    comprobantes_no_importados = []
    if solicitud_descarga.tipo_solicitud == 'CFDI' and solicitud_descarga.pendiente == False:
        descargas = Descarga.objects.filter(solicitud=solicitud_descarga)
        
        for descarga in descargas:
            importados, no_importados = salvar_xmls_from_zip_file(descarga.file_url, contribuyente.files_path, solicitud_descarga.tipo, contribuyente)
            comprobantes_importados.append(importados)
            comprobantes_no_importados.append(no_importados)

        solicitud_descarga.importada = True
        solicitud_descarga.save()
        return Response({"message":"Terminada","importados":comprobantes_importados, "no_importados":comprobantes_no_importados})
    else:
         return Response({"message":"Error","importados":comprobantes_importados, "no_importados":comprobantes_no_importados})
    
@api_view(['GET'])
def verificar_cancelados(request):
    print("Verificando Cancelados")
    solicitud = request.query_params.get('solicitud_id')
    solicitud_descarga = SolicitudDescarga.objects.get(id=solicitud)
    contribuyente = Contribuyente.objects.get(rfc=solicitud_descarga.rfc)
    if solicitud_descarga.tipo_solicitud == 'Metadata':
        descargas = Descarga.objects.filter(solicitud=solicitud_descarga)
        for descarga in descargas:
            validar_cancelados(descarga.file_url, contribuyente) 
    solicitud_descarga.pendiente = False
    solicitud_descarga.importada = True
    solicitud_descarga.save()
    return Response({"message":"Succesfully2"})


''' @api_view(['GET'])
def verificar_cancelados(request):
    solicitud = request.query_params.get('solicitud_id')
    print(solicitud)
    solicitud_descarga = SolicitudDescarga.objects.get(id=solicitud)
    contribuyente = Contribuyente.objects.get(rfc=solicitud_descarga.rfc)
    if solicitud_descarga.tipo == 'CANCELADOS' and solicitud_descarga.pendiente == False:
        descargas = Descarga.objects.filter(solicitud=solicitud_descarga)
        print(descargas)
        for descarga in descargas:
            validar_cancelados(descarga.file_url, contribuyente)
    
    return Response({"message":"Terminada"}) '''
    
class ComprobantesFiscalesRecibidosView(ListAPIView):

    serializer_class = ComprobanteFiscalSerializer
    def get_queryset(self):
        
        print(self.request.query_params)
        contribuyente_id = self.request.query_params.get('contribuyente_id')
        contribuyente = Contribuyente.objects.get(id=contribuyente_id)
        fecha_inicial = self.request.query_params.get('fecha_inicial')
        fecha_final = self.request.query_params.get('fecha_final')
        return ComprobanteFiscal.objects.get_recibidos(contribuyente, fecha_inicial, fecha_final).order_by('fecha')

class ComprobantesFiscalesEmitidosView(ListAPIView):
    
    serializer_class = ComprobanteFiscalSerializer
    def get_queryset(self):
        
        print(self.request.query_params)
        contribuyente_id = self.request.query_params.get('contribuyente_id')
        contribuyente = Contribuyente.objects.get(id=contribuyente_id)
        fecha_inicial = self.request.query_params.get('fecha_inicial')
        fecha_final = self.request.query_params.get('fecha_final')
        return ComprobanteFiscal.objects.get_emitidos(contribuyente, fecha_inicial, fecha_final)
    
@api_view(['GET'])
def descargar_archivo_xml(request):
    print("Descargando Archivo")
    comprobante_id = request.query_params['comprobante_id'] 
    comprobante = ComprobanteFiscal.objects.get(pk=comprobante_id)
    response = StreamingHttpResponse(file_iterator(comprobante.file_path), content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(comprobante.file_path)}'
    response['Content-Type'] = 'application/xml'
    #return JsonResponse({'message':'Descarga Masiva'})
    return response

@api_view(['GET'])
def imprimir_pdf(request):
    comprobante_id = request.query_params['comprobante_id'] 
    comprobante = ComprobanteFiscal.objects.get(pk=comprobante_id)
    with open(comprobante.file_path, 'r') as file:
        xml = file.read()
        pdf = print_pdf(xml)
    
    return HttpResponse(pdf, content_type='application/pdf')

@api_view(['GET'])
def imprimir_acuse(request):
    print("Imprimiendo Acuse")
    acuse = request.query_params
    comprobante = ComprobanteFiscal.objects.filter(uuid=acuse['uuid']).first()
    with open(comprobante.file_path, 'r') as file:
        xml = file.read()
        print(comprobante.file_path)
        pdf = print_acuse(acuse,xml)

    
    return HttpResponse(pdf, content_type='application/pdf')


@api_view(['GET'])
def validar_comprobante(request):
    print("Validando Comprobante")
    comprobante_id = request.query_params['comprobante_id']
    comprobante = ComprobanteFiscal.objects.get(pk=comprobante_id)
    print(comprobante)
    res = validar_cfdi(comprobante)
    return JsonResponse(res)
   

@api_view(['GET'])
def exportar_csv(request):
    print("Exportando CSV")

    contribuyente_id = request.query_params.get('contribuyente_id')
    contribuyente = Contribuyente.objects.get(id=contribuyente_id)
    fecha_inicial = request.query_params.get('fecha_inicial')
    fecha_final = request.query_params.get('fecha_final')
    tipo = request.query_params.get('tipo')

    comprobantes = []
    if tipo == 'EMITIDOS':
        comprobantes = ComprobanteFiscal.objects.get_emitidos_to_csv(contribuyente, fecha_inicial, fecha_final)
        
    if tipo == 'RECIBIDOS':
        comprobantes = ComprobanteFiscal.objects.get_recibidos_to_csv(contribuyente, fecha_inicial, fecha_final)

    df = pd.DataFrame(list(comprobantes.values('id','emisor','receptor','fecha','uuid','rfc_emisor','rfc_receptor','serie','folio','fecha_timbrado',
                                               'regimen_fiscal','regimen_fiscal_receptor','domicilio_fiscal','forma_pago','metodo_pago','uso_cfdi',
                                               'importe','descuento','subtotal','total_impuestos_trasladados','total_impuestos_retenidos',
                                               'total','moneda','tipo_cambio','tipo_de_comprobante')))
     # Generar el archivo CSV en memoria
    csv_buffer = df.to_csv(index=False)
    # Devolver el archivo CSV como respuesta HTTP
    response = HttpResponse(csv_buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="personas.csv"'
    return response


@api_view(['GET'])
def get_sat_comprobantes_impuestos(request):

    tipo = request.query_params.get('tipo')
    contribuyente = request.query_params.get('contribuyente')
    fecha_inicial = request.query_params.get('fecha_inicial')
    fecha_final = request.query_params.get('fecha_final')
    comprobantes = []
    if tipo == 'EMITIDOS':
        comprobantes = SatComprobanteImpuestos.objects.filter(emisor=contribuyente, fecha__date__range=[fecha_inicial, fecha_final]).order_by('fecha')
        serializer = SatComprobanteImpuestosSerializer(comprobantes, many=True)
        return Response({"data":serializer.data,"message":"OK"})
    if tipo == 'RECIBIDOS':
        comprobantes = SatComprobanteImpuestos.objects.filter(receptor=contribuyente, fecha__date__range=[fecha_inicial, fecha_final]).order_by('fecha')
        serializer = SatComprobanteImpuestosSerializer(comprobantes, many=True)
        return Response({"data":serializer.data,"message":"OK"})
       
    return Response({"data":[],"message":"EMPTY"})


@api_view(['GET'])
def  generar_comprobante_impuestos(request):
    print("Generando Comprobante Impuestos")
    print(request.query_params)
    tipo = request.query_params.get('tipo')
    contribuyente = request.query_params.get('contribuyente')
    fecha_inicial = request.query_params.get('fecha_inicial')
    fecha_final = request.query_params.get('fecha_final')
    make_comprobante_impuestos(tipo, contribuyente, fecha_inicial, fecha_final)
    return Response({"message":"Terminada"})


@api_view(['GET'])
def  get_referencias_pago(request):
    tipo = request.query_params.get('tipo')
    contribuyente = request.query_params.get('contribuyente')
    fecha_inicial = request.query_params.get('fecha_inicial')
    fecha_final = request.query_params.get('fecha_final')
    get_referencias(tipo, contribuyente, fecha_inicial, fecha_final)
    return Response({"message":"Terminada"})


@api_view(['GET'])
def get_sat_comprobantes_impuestos_ppd(request):

    tipo = request.query_params.get('tipo')
    contribuyente = request.query_params.get('contribuyente')
    fecha_inicial = request.query_params.get('fecha_inicial')
    fecha_final = request.query_params.get('fecha_final')
    comprobantes = []
    if tipo == 'EMITIDOS':
        comprobantes = SatComprobanteImpuestos.objects.filter(emisor=contribuyente,metodo_pago = 'PPD' , fecha_pago__range=[fecha_inicial, fecha_final]).order_by('fecha_pago')
        serializer = SatComprobanteImpuestosSerializer(comprobantes, many=True)
        return Response({"data":serializer.data,"message":"OK"})
    if tipo == 'RECIBIDOS':
        comprobantes = SatComprobanteImpuestos.objects.filter(receptor=contribuyente,metodo_pago = 'PPD', fecha_pago__range=[fecha_inicial, fecha_final]).order_by('fecha_pago')
        serializer = SatComprobanteImpuestosSerializer(comprobantes, many=True)
        return Response({"data":serializer.data,"message":"OK"})

    return Response({"message":"Terminada"})
        




@api_view(['GET'])
def exportar_impuestos_csv(request):
    contribuyente= request.query_params.get('contribuyente')
    fecha_inicial = request.query_params.get('fecha_inicial')
    fecha_final = request.query_params.get('fecha_final')
    tipo = request.query_params.get('tipo')

    comprobantes_list = []

    if tipo == 'EMITIDOS':
        comprobantes = SatComprobanteImpuestos.objects.filter(emisor=contribuyente, fecha__date__range=[fecha_inicial, fecha_final]).order_by('fecha')  
    if tipo == 'RECIBIDOS':
        comprobantes = SatComprobanteImpuestos.objects.filter(receptor=contribuyente, fecha__date__range=[fecha_inicial, fecha_final]).order_by('fecha')
    
    if tipo == 'PPD':
        comprobantes = SatComprobanteImpuestos.objects.filter(receptor=contribuyente, metodo_pago='PPD', fecha_pago__range=[fecha_inicial, fecha_final]).order_by('fecha_pago')

    df = pd.DataFrame(list(comprobantes.values('id','emisor','rfc_emisor','receptor','rfc_receptor','fecha','fecha_timbrado','uuid','serie','folio','forma_pago','metodo_pago','moneda',
                                               'tipo_cambio','tipo_comprobante','descuento','subtotal','total','iva_trasladado_porc','iva_trasladado_importe','iva_retenido_porc','iva_retenido_importe',
                                               'isr_retenido_porc','isr_retenido_importe','cancelado','total_impuestos_trasladados','total_impuestos_retenidos','aclaracion_referencia','fecha_pago','forma_de_pago','referencia_pago')))
    

    # Generar el archivo CSV en memoria
    csv_buffer = df.to_csv(index=False)
    # Devolver el archivo CSV como respuesta HTTP
    response = HttpResponse(csv_buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="personas.csv"'
    return response
