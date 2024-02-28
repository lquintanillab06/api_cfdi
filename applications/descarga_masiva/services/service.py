from  django.conf import settings
from .autenticacion import Autenticacion
from .fiel import Fiel
from .solicitadescarga import SolicitaDescarga
from .verificasolicituddescarga import VerificaSolicitudDescarga
from .validacioncfdi import Validacion
from .descargamasiva import DescargaMasiva
from applications.cfdi.services.encrypt_text import decrypt_text
import base64


def autenticacion(contribuyente):
    """Funcion para autenticar el usuario al webservice del SAT"""
    FIEL_KEY = contribuyente.llave_privada_firma
    FIEL_CER = contribuyente.certificado_digital_firma
    FIEL_PAS = contribuyente.password_key_firma
    cer_der = FIEL_CER
    key_der = FIEL_KEY  
    fiel = Fiel(cer_der, key_der, FIEL_PAS)
    auth = Autenticacion(fiel)
    token = auth.obtener_token()
    return token
    
def solicitar_descarga(contribuyente, tipo_solicitud, fecha_inicial, fecha_final, tipo ):
    """Funcion para solicitar la descarga masiva de CFDI"""
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
        solicitud = descarga.solicitar_descarga(token, rfc_solicitante=contribuyente.rfc, fecha_inicial=fecha_inicial, fecha_final=fecha_final,rfc_emisor=contribuyente.rfc, tipo_solicitud=tipo_solicitud, estado_comprobante="1")
    if tipo == 'RECIBIDOS':
        solicitud = descarga.solicitar_descarga(token, rfc_solicitante=contribuyente.rfc, fecha_inicial=fecha_inicial, fecha_final=fecha_final,rfc_receptor=contribuyente.rfc, tipo_solicitud=tipo_solicitud,estado_comprobante="1")
    # print(solicitud)
    return solicitud
   
def consultar_solicitud(contribuyente, solicitud):
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
    consulta = verificacion.verificar_descarga(token, solicitud.rfc, solicitud.solicitud_id)
    print("CONSULTA", consulta)
    estado_solicitud = int(consulta['estado_solicitud'])
    descargas = []
    descarga={"file_name":None,"file_url":None}
    if estado_solicitud == 3 and solicitud.pendiente == True:
        for paquete in consulta['paquetes']:
            descarga = DescargaMasiva(fiel)
            descarga = descarga.descargar_paquete(token, contribuyente.rfc, paquete)
            # print('PAQUETE',paquete)
            ''' with open('{}.zip'.format(paquete), 'wb') as f:
                f.write(base64.b64decode(descarga['paquete_b64'])) '''
            with open(f"{settings.MEDIA_ROOT}{paquete}.zip", 'wb') as f:
                f.write(base64.b64decode(descarga['paquete_b64']))  
                descarga["file_name"] = f"{paquete}.zip"
                descarga["file_url"] = f"{settings.MEDIA_ROOT}{paquete}.zip"
                descargas.append(descarga)
                
        return (consulta['estado_solicitud'],False,descargas)
    elif estado_solicitud > 3 and solicitud.pendiente == True:
        return (consulta['estado_solicitud'], False, [])
    else:
        return (consulta['estado_solicitud'],solicitud.pendiente,[])
    

def solicitar_descarga_uuid(contribuyente, uuid, fecha_inicial, fecha_final):
    """Funcion para solicitar la descarga masiva de CFDI"""
    FIEL_KEY = contribuyente.llave_privada_firma
    FIEL_CER = contribuyente.certificado_digital_firma
    FIEL_PAS = contribuyente.password_key_firma
    cer_der = FIEL_CER
    key_der = FIEL_KEY  
    fiel = Fiel(cer_der, key_der, FIEL_PAS)
    auth = Autenticacion(fiel)
    token = auth.obtener_token()
    descarga = SolicitaDescarga(fiel)
    solicitud = descarga.solicitar_descarga(token, tipo_solicitud='Metadata', uuid=uuid)
    # print(solicitud)
    return solicitud

def validar_cfdi(comprobante):
    validacion = Validacion()
    res = validacion.obtener_estado(comprobante.rfc_emisor, comprobante.rfc_receptor, str(comprobante.total), comprobante.uuid)
    print(res)
    return res



