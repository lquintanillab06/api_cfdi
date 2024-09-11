from  django.conf import settings
from .autenticacion import Autenticacion
from .fiel import Fiel
from .solicitadescarga import SolicitaDescarga
from .verificasolicituddescarga import VerificaSolicitudDescarga
from .validacioncfdi import Validacion
from .descargamasiva import DescargaMasiva
from applications.cfdi.services.encrypt_text import decrypt_text
import base64
from datetime import date, datetime
from ..models import SolicitudDescarga
from applications.cfdi.models import Contribuyente
from applications.descarga_masiva.models import Descarga
from applications.administracion_cfdi.services.services import salvar_xmls_from_zip_file


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
    '''    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(descarga)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") '''
    if tipo == 'EMITIDOS':
        solicitud = descarga.solicitar_descarga(token, rfc_solicitante=contribuyente.rfc, fecha_inicial=fecha_inicial, fecha_final=fecha_final,rfc_emisor=contribuyente.rfc, tipo_solicitud=tipo_solicitud )
    if tipo == 'RECIBIDOS':
        solicitud = descarga.solicitar_descarga(token, rfc_solicitante=contribuyente.rfc, fecha_inicial=fecha_inicial, fecha_final=fecha_final,rfc_receptor=contribuyente.rfc, tipo_solicitud=tipo_solicitud)
    #print("/////////////////////////////////////////////")    
    #print(solicitud)
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


    
def descarga_cancelados(contribuyente, tipo_solicitud, fecha_inicial, fecha_final ):
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

    descarga.solicitar_descarga(token, rfc_solicitante=contribuyente.rfc, fecha_inicial=fecha_inicial, fecha_final=fecha_final,rfc_emisor=contribuyente.rfc,tipo_solicitud=tipo_solicitud, estado_comprobante="0")

    # print(solicitud)
    return solicitud

''' def solicitar_descarga(contribuyente, tipo_solicitud, fecha_inicial, fecha_final, tipo ):
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
        solicitud = descarga.solicitar_descarga(token, rfc_solicitante=contribuyente.rfc, fecha_inicial=fecha_inicial, fecha_final=fecha_final,rfc_emisor=contribuyente.rfc, tipo_solicitud=tipo_solicitud )
    if tipo == 'RECIBIDOS':
        solicitud = descarga.solicitar_descarga(token, rfc_solicitante=contribuyente.rfc, fecha_inicial=fecha_inicial, fecha_final=fecha_final,rfc_receptor=contribuyente.rfc, tipo_solicitud=tipo_solicitud)
    #print("/////////////////////////////////////////////")    
    #print(solicitud)
    return solicitud '''

def descarga_auto():
    print(f"Task executed at {datetime.now()}")
    tipo_descarga = 'CFDI'
    tipo = 'RECIBIDOS'
    contribuyente = Contribuyente.objects.get(pk=2)
    hoy = date.today()
    fecha_inicial = datetime(hoy.year, hoy.month, hoy.day - 1, 00, 00, 00)
    fecha_final = datetime(hoy.year, hoy.month, hoy.day - 1, 23, 59, 59)    
    solicitud = solicitar_descarga(contribuyente, tipo_descarga, fecha_inicial, fecha_final, tipo)
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

def consultar_solicitud_auto():
    print(f"Consulting at {datetime.now()}")
    hoy = date.today()
    contribuyente = Contribuyente.objects.get(pk=2)
    sol = SolicitudDescarga.objects.filter(pendiente=True,date_created__date=hoy,rfc=contribuyente.rfc) 
    if sol:
        solicitud = sol
        print(solicitud.id)
        estado, pendiente, descargas = consultar_solicitud(contribuyente, solicitud)
        solicitud.estatus = estado
        solicitud.pendiente = pendiente
        solicitud.save()

        if len(descargas) > 0:
            for descarga in descargas:
                descarga_bd = solicitud[0].descargas.create(tipo=solicitud[0].tipo_solicitud,file_name=descarga['file_name'],file_url=descarga['file_url'])
                descarga_bd.save()


def cargar_xmls_auto():
    print(f"Importing xml files at {datetime.now()}")
    hoy = date.today()
    contribuyente = Contribuyente.objects.get(pk=2)
    sol = SolicitudDescarga.objects.filter(pendiente=False,importada=False,date_created__date=hoy,estatus=3, rfc=contribuyente.rfc)
    comprobantes_importados = []
    comprobantes_no_importados = []
    if sol:
        solicitud = sol[0]
        print(solicitud.__dict__)
        descargas = Descarga.objects.filter(solicitud=solicitud)
        for descarga in descargas:
            importados, no_importados = salvar_xmls_from_zip_file(descarga.file_url, contribuyente.files_path, solicitud.tipo, contribuyente)
            comprobantes_importados.append(importados)
            comprobantes_no_importados.append(no_importados)

        solicitud.importada = True
        solicitud.save() 