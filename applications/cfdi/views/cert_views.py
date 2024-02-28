import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework import status
from ..models import Contribuyente
from ..services.encrypt_text import generate_key,encrypt_text

@api_view(['GET'])
def get_key(request,contribuyente_id):
   contribuyente = Contribuyente.objects.filter(pk=contribuyente_id).first()
   return Response({"Value":"Test"})

@api_view(['GET'])
def get_cert(request,contribuyente_id):
    contribuyente = Contribuyente.objects.filter(pk=contribuyente_id).first()
    cert_file = contribuyente.certificado_digital
    cert = base64.b64encode(cert_file)
    return Response({"Value":"Test"})

@api_view(['GET'])
def get_pfx(request,contribuyente_id):
    contribuyente = Contribuyente.objects.filter(pk=contribuyente_id).first()
    pfx_file = contribuyente.certificado_digital_pfx
    cert = base64.b64encode(pfx_file)
    return Response({"Value":"Test"})

@api_view(['GET'])
def get_numero_certificado(request,contribuyente_id):
    contribuyente = Contribuyente.objects.filter(pk=contribuyente_id).first()
    numero_certificado = contribuyente.numero_certificado
    print(request.accepted_media_type)
    return Response({"Value":numero_certificado})

@api_view(['POST'])
def set_numero_certificado(request,contribuyente_id):
    contribuyente = Contribuyente.objects.filter(pk=contribuyente_id).first()
    numero_certificado = request.query_params['numero_certificado']
    contribuyente.numero_certificado = numero_certificado
    contribuyente.save()
    return Response({"Value":"The number was updated successfully"})

class UploadCertView(APIView):
    
    parser_classes=[FileUploadParser]

    def post(self, request,contribuyente_id, filename, format=None):
        cert_file  = request.data['file'].read()
        contribuyente = Contribuyente.objects.filter(pk=contribuyente_id).first()
        contribuyente.certificado_digital = cert_file
        contribuyente.save()
        return Response({"Message": "The certified was updated successfully"})
    
class UploadCertFirmaView(APIView):
        
    parser_classes=[FileUploadParser]

    def post(self, request,contribuyente_id, filename, format=None):
        cert_file  = request.data['file'].read()
        contribuyente = Contribuyente.objects.filter(pk=contribuyente_id).first()
        contribuyente.certificado_digital_firma = cert_file
        contribuyente.save()
        return Response({"Message": "The certified was updated successfully"})
    
class UploadKeyFirmaView(APIView):
    
    parser_classes=[FileUploadParser]

    def post(self, request,contribuyente_id, filename, format=None):
        print(type(request.data['file']))
        key_file  = request.data['file'].read()
        contribuyente = Contribuyente.objects.filter(pk=contribuyente_id).first()
        contribuyente.llave_privada_firma = key_file
        contribuyente.save()
        return Response({"Message": "The key was updated successfully"})
    

class UploadKeyView(APIView):

    parser_classes=[FileUploadParser]

    def post(self, request,contribuyente_id, filename, format=None):
        print(type(request.data['file']))
        key_file  = request.data['file'].read()
        contribuyente = Contribuyente.objects.filter(pk=contribuyente_id).first()
        contribuyente.llave_privada = key_file
        contribuyente.save()
        return Response({"Texto": "The key was updated successfully"})
    

class UploadPfxView(APIView):
    
    parser_classes=[FileUploadParser]

    def post(self, request,contribuyente_id, filename, format=None):
        print(type(request.data['file']))
        pfx_file  = request.data['file'].read()
        contribuyente = Contribuyente.objects.filter(pk=contribuyente_id).first()
        contribuyente.certificado_digital_pfx= pfx_file
        contribuyente.save()
        print(request.accepted_media_type)
        return Response({"Message": "The pfx was updated successfully"},status= status.HTTP_200_OK)
    

@api_view(['GET'])
def get_encrypted_key(request):
    contribuyente_id = request.query_params['contribuyente_id']
    contribuyente = Contribuyente.objects.get(pk=contribuyente_id)
    print(contribuyente.clave)
    key = generate_key()
    contribuyente.encrypted_key = key.decode()
    contribuyente.save()
    return Response("Successfully get encrypted key")
