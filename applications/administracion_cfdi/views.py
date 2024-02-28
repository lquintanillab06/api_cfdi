from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse


from django.http import StreamingHttpResponse
from .services.services import salvar_xmls_from_zip_file
from .services.print_services import print_pdf
from applications.descarga_masiva.services.service import validar_cfdi
from applications.commons.utils.utils_file import file_iterator
import os   

from applications.descarga_masiva.models import Descarga, SolicitudDescarga 
from applications.cfdi.models import Contribuyente
from .models import ComprobanteFiscal
from .serializers import ComprobanteFiscalSerializer
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
    
class ComprobantesFiscalesRecibidosView(ListAPIView):

    serializer_class = ComprobanteFiscalSerializer
    def get_queryset(self):
        
        print(self.request.query_params)
        contribuyente_id = self.request.query_params.get('contribuyente_id')
        contribuyente = Contribuyente.objects.get(id=contribuyente_id)
        fecha_inicial = self.request.query_params.get('fecha_inicial')
        fecha_final = self.request.query_params.get('fecha_final')
        return ComprobanteFiscal.objects.get_recibidos(contribuyente, fecha_inicial, fecha_final)

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






