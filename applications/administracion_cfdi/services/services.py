from ..models import ComprobanteFiscal, ComprobanteFiscalConcepto, ComprobanteFiscalImpuesto, ComprobanteFiscalConceptoImpuesto, ComprobanteFiscalCancelado
from zipfile import ZipFile
from lxml import etree as ET
from datetime import datetime
import os
import csv

def salvar_xmls_from_zip_file(zip_file_path, files_path, tipo, contribuyente):


    try:
        if not os.path.exists(files_path):
            os.makedirs(files_path)
    except OSError:
        print('Error: Creating directory. ' + files_path)

    importados = []
    no_importados = []
    comprobantes = []
    with ZipFile(zip_file_path, 'r') as zip:

        counter = 0

        for  name in zip.namelist():
            counter += 1
            print("*"*50)
            with zip.open(name) as file:

                xml = file.read()

                namespaces = {
                    "cfdi": "http://www.sat.gob.mx/cfd/4",
                    "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital"
                }

                root = ET.fromstring(xml.decode('utf-8'))  
                version = root.xpath('//cfdi:Comprobante/@Version', namespaces=namespaces)

                if len(version) > 0:
                    version_cfdi = version[0]

                else:
                    namespaces = {
                        "cfdi": "http://www.sat.gob.mx/cfd/3",
                        "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital"
                    }
                    version = root.xpath('//cfdi:Comprobante/@Version', namespaces=namespaces)
                    version_cfdi = version[0]

                rfc_emisor = root.xpath('//cfdi:Comprobante/cfdi:Emisor/@Rfc', namespaces=namespaces)
                rfc_receptor = root.xpath('//cfdi:Comprobante/cfdi:Receptor/@Rfc', namespaces=namespaces)
                fecha = root.xpath('//cfdi:Comprobante/@Fecha', namespaces=namespaces)
                uuid = root.xpath('//tfd:TimbreFiscalDigital/@UUID', namespaces=namespaces)[0]

                if (tipo == 'RECIBIDOS' and rfc_receptor[0] == contribuyente.rfc) or (tipo == 'EMITIDOS' and rfc_emisor[0] == contribuyente.rfc):

                    fecha = datetime.fromisoformat(fecha[0])
                    path_save = os.path.join(files_path,str(fecha.year),str(fecha.month),str(fecha.day),tipo)

                    try:
                        if not os.path.exists(path_save):
                            os.makedirs(path_save)
                    except OSError:
                        print('Error: Creating directory. ' + path_save)

                    zip.extract(name, path_save)

                    comprobante = ComprobanteFiscal()
                    comprobante.rfc_emisor = root.xpath('//cfdi:Comprobante/cfdi:Emisor/@Rfc', namespaces=namespaces)[0]
                    comprobante.emisor = root.xpath('//cfdi:Comprobante/cfdi:Emisor/@Nombre', namespaces=namespaces)[0]
                    comprobante.rfc_receptor = root.xpath('//cfdi:Comprobante/cfdi:Receptor/@Rfc', namespaces=namespaces)[0]
                    comprobante.receptor = root.xpath('//cfdi:Comprobante/cfdi:Receptor/@Nombre', namespaces=namespaces)[0]  
                    comprobante.fecha = fecha

                    if version_cfdi == '4.0':
                        comprobante.regimen_fiscal = root.xpath('//cfdi:Comprobante/cfdi:Emisor/@RegimenFiscal', namespaces=namespaces)[0]
                        comprobante.regimen_fiscal_receptor = root.xpath('//cfdi:Comprobante/cfdi:Receptor/@RegimenFiscalReceptor', namespaces=namespaces)[0]
                        comprobante.domicilio_fiscal = root.xpath('//cfdi:Comprobante/cfdi:Receptor/@DomicilioFiscalReceptor', namespaces=namespaces)[0]     

                    comprobante.uuid = root.xpath('//tfd:TimbreFiscalDigital/@UUID', namespaces=namespaces)[0]
                    serie = root.xpath('//cfdi:Comprobante/@Serie', namespaces=namespaces)
                    
                    if len(serie) > 0:
                        comprobante.serie = serie[0]

                    folio = root.xpath('//cfdi:Comprobante/@Folio', namespaces=namespaces)
                    if len(folio) > 0:
                        comprobante.folio = folio[0]
             
                    forma_pago = root.xpath('//cfdi:Comprobante/@FormaPago', namespaces=namespaces)

                    if len(forma_pago) > 0:
                        comprobante.forma_pago = forma_pago[0]
                   
                    metodo_pago = root.xpath('//cfdi:Comprobante/@MetodoPago', namespaces=namespaces)
                    if len(metodo_pago) > 0:
                        comprobante.metodo_pago = metodo_pago[0]
                
                    comprobante.uso_cfdi =  root.xpath('//cfdi:Comprobante/cfdi:Receptor/@UsoCFDI', namespaces=namespaces)[0]
                    comprobante.importe = root.xpath('//cfdi:Comprobante/@Total', namespaces=namespaces)[0]

                    descuento = root.xpath('//cfdi:Comprobante/@Descuento', namespaces=namespaces)
                    if len(descuento) > 0:
                        comprobante.descuento = descuento[0]

                    comprobante.subtotal = root.xpath('//cfdi:Comprobante/@SubTotal', namespaces=namespaces)[0]
                    comprobante.total = root.xpath('//cfdi:Comprobante/@Total', namespaces=namespaces)[0]
                    comprobante.moneda = root.xpath('//cfdi:Comprobante/@Moneda', namespaces=namespaces)[0]

                    tipo_cambio = root.xpath('//cfdi:Comprobante/@TipoCambio', namespaces=namespaces)
                    if len(tipo_cambio) > 0:
                        comprobante.tipo_cambio = tipo_cambio[0]
   
                    comprobante.tipo_de_comprobante = root.xpath('//cfdi:Comprobante/@TipoDeComprobante', namespaces=namespaces)[0]
                    comprobante.fecha_timbrado = root.xpath('//tfd:TimbreFiscalDigital/@FechaTimbrado', namespaces=namespaces)[0]
                    comprobante.file_name = name
                    comprobante.file_path = f"{path_save}/{name}" 
                    comprobante.contribuyente = contribuyente

                    # Comprobante Impuestos
                    comprobante_impuestos_nodo = root.xpath('//cfdi:Comprobante/cfdi:Impuestos', namespaces=namespaces)
                    if len(comprobante_impuestos_nodo) > 0:
                        comprobante_impuestos = comprobante_impuestos_nodo[0].attrib
                        if 'TotalImpuestosTrasladados' in comprobante_impuestos:
                            comprobante.total_impuestos_trasladados = comprobante_impuestos['TotalImpuestosTrasladados']
                        if 'TotalImpuestosRetenidos' in comprobante_impuestos:
                            comprobante.total_impuestos_retenidos = comprobante_impuestos['TotalImpuestosRetenidos']

                    try:
                        comprobantes.append(comprobante)
                        #comprobante.save()
                        #importados.append(uuid)
                        #print('Comprobante guardado'+uuid)
                    except Exception as e:
                        print(e)
                        print('Error al guardar el comprobante')
                        #no_importados.append(uuid)
                        print('Comprobante No importado'+uuid)
                        continue
                else:
                    print('El comprobante no pertenece al contribuyente')
                    #no_importados.append(uuid)
        #print(comprobantes)
        ComprobanteFiscal.objects.bulk_create(comprobantes,update_conflicts=True, update_fields=['uuid'])
        print('Total de comprobantes '+str(counter))    
                                       
    return importados, no_importados


def validar_cancelados(zip_file_path, contribuyente):

    print('Validando cancelados')
    with ZipFile(zip_file_path, 'r') as zip:

        for  name in zip.namelist():
            with zip.open(name) as file:

                lines = file.readlines()

                for line in lines:
                    if not line == lines[0]:
                       row = line.decode('utf-8').split('~')   
                       if len(row) > 11:
                            if row[10] == '0' :
                                print(row[0])
                                print(row[10])
                                print(row[11])
                                found = ComprobanteFiscal.objects.filter(uuid=row[0], contribuyente=contribuyente).first()
                                print(found)
                                print("_"*50)
                                if found != None:
                                    found_cancelado = ComprobanteFiscalCancelado.objects.filter(comprobante_fiscal=found).first()
                                    if found_cancelado == None:
                                        cancelado = ComprobanteFiscalCancelado()
                                        cancelado.comprobante_fiscal = found
                                        cancelado.fecha_cancelacion = row[11]
                                        cancelado.rfc_receptor = row[3]
                                        cancelado.nombre_receptor = row[4]
                                        cancelado.rfc_emisor = row[1]
                                        cancelado.nombre_emisor = row[2]
                                        cancelado.uuid = row[0]
                                        cancelado.cancelado = True
                                        cancelado.save()  
                                        found.cancelado = True
                                        found.save()  
                                        print('Comprobante cancelado') 
                            
                    
