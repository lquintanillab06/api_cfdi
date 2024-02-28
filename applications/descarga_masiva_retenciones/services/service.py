
from  django.conf import settings
from .autenticacion import Autenticacion
from .fiel import Fiel

from .solicitadescarga import SolicitaDescarga
from .verificasolicituddescarga import VerificaSolicitudDescarga
from .descargamasiva import DescargaMasiva 
from applications.cfdi.services.encrypt_text import decrypt_text
import base64

def solicitar_descarga(contribuyente, tipo_solicitud, fecha_inicial, fecha_final, tipo ):
    """Funcion para autenticar el usuario al webservice del SAT"""
    password = decrypt_text(contribuyente.password_key_firma.encode(),contribuyente.encrypted_key.encode())
    FIEL_KEY = contribuyente.llave_privada_firma
    FIEL_CER = contribuyente.certificado_digital_firma
    FIEL_PAS = password
    cer_der = FIEL_CER
    key_der = FIEL_KEY  
    fiel = Fiel(cer_der, key_der, FIEL_PAS)
    auth = Autenticacion(fiel)
    token = auth.obtener_token()
    descarga = SolicitaDescarga(fiel)
    if tipo == 'EMITIDOS':
        # solicitud = descarga.solicitar_descarga(token, rfc_solicitante=contribuyente.rfc, fecha_inicial=fecha_inicial, fecha_final=fecha_final,rfc_emisor=contribuyente.rfc, tipo_solicitud=tipo_solicitud, estado_comprobante="1")
        solicitud = descarga.solicitar_descarga(token, rfc_solicitante=contribuyente.rfc, fecha_inicial=fecha_inicial, fecha_final=fecha_final,rfc_emisor=contribuyente.rfc, tipo_solicitud=tipo_solicitud)
    if tipo == 'RECIBIDOS':
        solicitud = descarga.solicitar_descarga(token, rfc_solicitante=contribuyente.rfc, fecha_inicial=fecha_inicial, fecha_final=fecha_final,rfc_receptor=contribuyente.rfc, tipo_solicitud=tipo_solicitud)
    print(solicitud)
    return solicitud

    # {'id_solicitud': '9c12ed31-4e85-4297-bf03-f243bccd09ee', 'cod_estatus': '5000', 'mensaje': 'Solicitud Aceptada'} LQB QUBL790930A69

    # {'id_solicitud': '490ac669-f3e6-4a62-a1bb-19ce0b59383a', 'cod_estatus': '5000', 'mensaje': 'Solicitud Aceptada'} PAGC PAGC721120L48

    # {'id_solicitud': '38bd2ded-6863-4db9-b0f9-a64a5222316a', 'cod_estatus': '5000', 'mensaje': 'Solicitud Aceptada'} PAGC

    # {'id_solicitud': '5384a2cb-1d45-4eb9-9254-068f74fdf063', 'cod_estatus': '5000', 'mensaje': 'Solicitud Aceptada'} PAGC

    # {'id_solicitud': 'f989cdea-4b58-4f57-8a93-174599dbe4b2', 'cod_estatus': '5000', 'mensaje': 'Solicitud Aceptada'} PAGC

    # {'id_solicitud': 'fe5b12b2-faae-4829-90d7-3c1030a23a2e', 'cod_estatus': '5000', 'mensaje': 'Solicitud Aceptada'} PAGC
    #{'id_solicitud': '5519daa8-836b-43ab-bd35-7622c0339025', 'cod_estatus': '5000', 'mensaje': 'Solicitud Aceptada'} PAGC
   # {'cod_estatus': '5000', 'estado_solicitud': '1', 'codigo_estado_solicitud': '5000', 'numero_cfdis': '0', 'mensaje': 'Solicitud Aceptada', 'paquetes': []}


def consultar_solicitud(contribuyente):
    """Funcion para consultar el estatus de la solicitud"""
    password = decrypt_text(contribuyente.password_key_firma.encode(),contribuyente.encrypted_key.encode())
    FIEL_KEY = contribuyente.llave_privada_firma
    FIEL_CER = contribuyente.certificado_digital_firma
    FIEL_PAS =  password
    cer_der = FIEL_CER
    key_der = FIEL_KEY  
    fiel = Fiel(cer_der, key_der, FIEL_PAS)
    verificacion = VerificaSolicitudDescarga(fiel)
    auth = Autenticacion(fiel)
    token = auth.obtener_token()
    consulta = verificacion.verificar_descarga(token, 'PAGC721120L48', '5519daa8-836b-43ab-bd35-7622c0339025')
    print("CONSULTA", consulta)




  
   
   