from applications.administracion_cfdi.models import ComprobanteFiscal
from django.db.models import Q
from decimal import Decimal
from ..models import SatComprobanteImpuestos
from lxml import etree as ET
import pandas as pd
import numpy as np
import requests
import time
import os




def make_comprobante_impuestos(tipo , contribuyente, fecha_inicial, fecha_final):

    # Configurar pandas para mostrar todo el DataFrame
    pd.set_option('display.max_rows', None)   # Muestra todas las filas
    pd.set_option('display.max_columns', None)  # Muestra todas las columnas
    #pd.set_option('display.max_colwidth', None)  # Muestra el contenido completo de cada columna
    pd.set_option('display.width', None)  # Ajusta el ancho para que se ajuste automáticamente
    pd.options.mode.copy_on_write = True

    if tipo == 'RECIBIDOS':
        comprobantes = ComprobanteFiscal.objects.filter( ~Q(tipo_de_comprobante='T'),receptor=contribuyente, fecha__date__range=[fecha_inicial,fecha_final])
    if tipo == 'EMITIDOS':
        comprobantes = ComprobanteFiscal.objects.filter( ~Q(tipo_de_comprobante='T'),emisor=contribuyente, fecha__date__range=[fecha_inicial,fecha_final])

    counter = 0
    impuestos_list =[]
    for comprobante in comprobantes:
        counter +=1

        with open(comprobante.file_path, 'r') as file:
            xml= file.read()
        
            namespaces = {
                "cfdi": "http://www.sat.gob.mx/cfd/4",
                "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital",
                "pago20":"http://www.sat.gob.mx/Pagos20"
            }
            root = ET.fromstring(xml)
            version = root.xpath('//cfdi:Comprobante/@Version', namespaces=namespaces)
            rfc_emisor = root.xpath('//cfdi:Comprobante/cfdi:Emisor/@Rfc', namespaces=namespaces)

            timbrado = root.find('.//tfd:TimbreFiscalDigital', namespaces).attrib
            
            comprobante_impuestos_nodo = root.xpath('//cfdi:Comprobante/cfdi:Impuestos', namespaces=namespaces)
            total_impuestos_trasladados = 0
            total_impuestos_retenidos = 0
            base = 0
            base_excenta = 0
            if len(comprobante_impuestos_nodo) > 0:
                comprobante_impuestos = comprobante_impuestos_nodo[0].attrib
                if 'TotalImpuestosTrasladados' in comprobante_impuestos:
                    total_impuestos_trasladados = comprobante_impuestos['TotalImpuestosTrasladados']
                    traslado_nodo = root.xpath('//cfdi:Comprobante/cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado', namespaces=namespaces)
                    ''' if len(traslado_nodo) >0:
                        trd = traslado_nodo[0].attrib
                        print(trd)
                        base = trd['Base'] '''
                    if len(traslado_nodo) >0:
                        for trd_nodo in traslado_nodo:
                            trd = trd_nodo.attrib
                            #print(trd)
                            if trd['TasaOCuota']=='0.000000':
                                base_excenta += Decimal(trd['Base'])
                            if trd['TasaOCuota']=='0.160000':
                                base += Decimal(trd['Base'])
                            #print(total_impuestos_trasladados)
                                #print(total_impuestos_trasladados)
                    else:
                        base = comprobante.subtotal
                if 'TotalImpuestosRetenidos' in comprobante_impuestos:
                    total_impuestos_retenidos = comprobante_impuestos['TotalImpuestosRetenidos']
                    if 'TotalImpuestosTrasladados' not in comprobante_impuestos:
                        base = comprobante.subtotal
                    #print(total_impuestos_retenidos)

            # Comprobante Dictionary
            comprobante_dict = {
                    'comprobante':comprobante.id,
                    'rfc_receptor': comprobante.rfc_receptor,
                    'receptor': comprobante.receptor,
                    'rfc_emisor': comprobante.rfc_emisor,
                    'emisor': comprobante.emisor,
                    'fecha':comprobante.fecha,
                    'uuid': comprobante.uuid,
                    'serie':comprobante.serie,
                    'folio':comprobante.folio,
                    'forma_pago':comprobante.forma_pago,
                    'metodo_pago':comprobante.metodo_pago,
                    'uso_cfdi': comprobante.uso_cfdi,
                    'moneda':comprobante.moneda,
                    'base': base,
                    'base_excenta': base_excenta,
                    'total_impuestos_trasladados': total_impuestos_trasladados,
                    'total_impuestos_retenidos': total_impuestos_retenidos,
                    'tipo_cambio': comprobante.tipo_cambio if comprobante.tipo_cambio else 1.00,
                    'tipo_comprobante': comprobante.tipo_de_comprobante,
                    'descuento': comprobante.descuento,
                    'subtotal': comprobante.subtotal,
                    'total': comprobante.total,
                    'cancelado':comprobante.cancelado,
                    'fecha_timbrado': timbrado['FechaTimbrado']
                }

            # Comprobante Impuestos por concepto
            traslados = root.xpath('//cfdi:Comprobante/cfdi:Conceptos/cfdi:Concepto/cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado', namespaces=namespaces)

            for traslado_nodo in traslados:	
                traslado = traslado_nodo.attrib
                impuestos_list.append({**comprobante_dict,**traslado,"clasificacion":"Traslado"})
       
            
            retenciones = root.xpath('//cfdi:Comprobante/cfdi:Conceptos/cfdi:Concepto/cfdi:Impuestos/cfdi:Retenciones/cfdi:Retencion', namespaces=namespaces)

            for retencion_nodo in retenciones :
                retencion = retencion_nodo.attrib
                impuestos_list.append({**comprobante_dict,**retencion,"clasificacion":"Retencion"})
     

        if comprobante.tipo_de_comprobante == 'P':
            
            totales_nodo = retenciones = root.xpath('//pago20:Totales', namespaces=namespaces)    
            totales = totales_nodo[0].attrib

            comprobante_dict['subtotal'] = totales['TotalTrasladosBaseIVA16']
            comprobante_dict['total'] = totales['MontoTotalPagos']
            comprobante_dict['base'] = totales['TotalTrasladosBaseIVA16']
            comprobante_dict['total_impuestos_trasladados'] = totales['TotalTrasladosImpuestoIVA16']


            traslados = retenciones = root.xpath('//pago20:TrasladoP', namespaces=namespaces)
            for traslado_nodo in traslados:
                traslado = traslado_nodo.attrib
                comprobante_dict['total_impuestos_retenidos'] = 0
                traslado_dict = {
                        "Base":traslado['BaseP'] if 'BaseP' in traslado else 0,
                        #"Importe": traslado['ImporteP'] if 'ImporteP' in traslado else 0,
                        "Importe":totales['TotalTrasladosImpuestoIVA16'],
                        "Impuesto": traslado['ImpuestoP'] if 'ImpuestoP' in traslado else 0,
                        "TasaOCuota": traslado['TasaOCuotaP'] if 'TasaOCuotaP' in traslado else 0,
                        "TipoFactor": traslado['TipoFactorP'] if 'TipoFactorP' in traslado else 0
                    }
                impuestos_list.append({**comprobante_dict,**traslado_dict,"clasificacion":"Traslado"})

    if len(impuestos_list) > 0:
        
        df = pd.DataFrame(impuestos_list)
        df['Importe']= df['Importe'].astype(float)
    
        df_impuesto = df.groupby(['comprobante','Impuesto','TipoFactor','TasaOCuota'])['Importe',].sum().reset_index()
        df_impuesto = df_impuesto.rename(columns={'Importe': 'SumaImporte'})

        df_new = df.merge(df_impuesto, on=['comprobante','Impuesto','TipoFactor','TasaOCuota'])
        df_new['TipoImpuesto'] = np.where(df_new['Impuesto'] == '002','IVA', 'ISR')

        df_unique_first = df_new.drop_duplicates(subset=['comprobante','Impuesto','TipoFactor','TasaOCuota'], keep='first')
        df_unique_first['TipoImpuesto'] = np.where(df_unique_first['Impuesto'] == '002','IVA', 'ISR')
        df_unique_first['Estatus'] = np.where (df_unique_first['cancelado'] , 'Cancelado','Vigente') 
        df_unique_first['Trasladado%'] = np.where((df_unique_first['Impuesto']=='002') & (df_unique_first['clasificacion'] == 'Traslado'), df_unique_first['TasaOCuota'],0).astype(float)
        df_unique_first['Trasladado$'] = np.where((df_unique_first['Impuesto']=='002') & (df_unique_first['clasificacion'] == 'Traslado'), df_unique_first['SumaImporte'],0)
        df_unique_first['RetencionIva%'] = np.where((df_unique_first['Impuesto']=='002') & (df_unique_first['clasificacion'] == 'Retencion'), df_unique_first['TasaOCuota'],0).astype(float)
        df_unique_first['RetencionIva$'] = np.where((df_unique_first['Impuesto']=='002') & (df_unique_first['clasificacion'] == 'Retencion'), df_unique_first['SumaImporte'],0)
        df_unique_first['RetencionIsr%'] = np.where((df_unique_first['Impuesto']=='001') & (df_unique_first['clasificacion'] == 'Retencion'), df_unique_first['TasaOCuota'],0).astype(float)
        df_unique_first['RetencionIsr$'] = np.where((df_unique_first['Impuesto']=='001') & (df_unique_first['clasificacion'] == 'Retencion'), df_unique_first['SumaImporte'],0)

        df_acum = df_unique_first.groupby('comprobante').agg({
            'Trasladado%':'sum',
            'Trasladado$':'sum',
            'RetencionIva%':'sum',
            'RetencionIva$':'sum',
            'RetencionIsr%':'sum',
            'RetencionIsr$':'sum'
        }).reset_index()

 
        

        df_acum = df_acum.rename(columns={'Estatus':'estado','Trasladado$': 'iva_trasladado_importe','Trasladado%': 'iva_trasladado_porc','RetencionIva$': 'iva_retenido_importe','RetencionIva%': 'iva_retenido_porc','RetencionIsr$': 'isr_retenido_importe','RetencionIsr%': 'isr_retenido_porc'})

        #df_unique_first = df_unique_first.rename(columns={'Base':'base'})
        df_inter = df_unique_first.merge(df_acum,on='comprobante')


        df_result = df_inter.drop_duplicates(subset=['comprobante'], keep='first')
    
        df_result['iva_trasladado_importe'] = df_result['iva_trasladado_importe'].apply(lambda x: '{:.2f}'.format(x))

        #columnas = ['descuento','subtotal','total','base','iva_trasladado_importe','iva_retenido_importe','isr_retenido_importe','total_impuestos_trasladados','total_impuestos_retenidos']

        ''' for columna in columnas:
            df_result[columna] = df_result['tipo_cambio'].astype(float)* df_result[columna].astype(float) '''


        columns =['comprobante','rfc_receptor','receptor','rfc_emisor','emisor','fecha','fecha_timbrado','uuid','serie','folio',
                    'forma_pago','metodo_pago','uso_cfdi','moneda','total_impuestos_trasladados','total_impuestos_retenidos',
                    'tipo_cambio','tipo_comprobante','descuento','subtotal','total','base','cancelado','iva_trasladado_importe',
                    'iva_trasladado_porc','iva_retenido_importe','iva_retenido_porc','isr_retenido_importe','isr_retenido_porc','base_excenta']
        
        df_def = df_result[columns]
        dict = df_def.to_dict(orient='records')
        comprobantes_impuestos = [SatComprobanteImpuestos(**comprobante) for comprobante in dict]
        SatComprobanteImpuestos.objects.bulk_create(comprobantes_impuestos,update_conflicts=True, update_fields=['uuid'])
   
    print("Files:", counter)


def get_referencias(tipo, contribuyente, fecha_inicial, fecha_final):   

    if tipo == 'RECIBIDOS':
        get_referencias_recibidos(contribuyente, fecha_inicial, fecha_final)
    
    if tipo == 'EMITIDOS':
        get_referencias_emitidos(contribuyente, fecha_inicial, fecha_final)
    

def get_referencias_recibidos(receptor, fecha_inicial, fecha_final):
    # Captura el tiempo inicial
    start_time = time.time()  

    comprobantes = SatComprobanteImpuestos.objects.filter(receptor=receptor, fecha__date__range=[fecha_inicial, fecha_final])
    df_comprobantes = pd.DataFrame(list(comprobantes.values('uuid','receptor','emisor','fecha','total','comprobante')))

    url = os.getenv('URL_API_CXP')
    params = {
        "fecha_inicial":fecha_inicial,
        "fecha_final": fecha_final,     
        }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if len(data['data']) > 0:
            df = pd.DataFrame(data['data'])
            df_new = df.merge(df_comprobantes, on=['uuid'])
            dict = df_new.to_dict(orient='records')

            lista_comprobantes = []
            for item in dict:
                comprobante = SatComprobanteImpuestos.objects.get(comprobante=item['comprobante'])
                comprobante.fecha_pago = item['fecha_pago']
                comprobante.forma_de_pago = item['forma_de_pago']
                comprobante.referencia_pago = item['referencia']
                comprobante.tipo_de_cambio_pago = Decimal(item['tipo_de_cambio_pago'])
        
                comprobante.descuento = comprobante.descuento * comprobante.tipo_de_cambio_pago
                comprobante.subtotal = comprobante.subtotal * comprobante.tipo_de_cambio_pago
                comprobante.total = comprobante.total * comprobante.tipo_de_cambio_pago
                comprobante.base = comprobante.base * comprobante.tipo_de_cambio_pago
                comprobante.iva_trasladado_importe = comprobante.iva_trasladado_importe * comprobante.tipo_de_cambio_pago
                comprobante.iva_retenido_importe = comprobante.iva_retenido_importe * comprobante.tipo_de_cambio_pago
                comprobante.isr_retenido_importe = comprobante.isr_retenido_importe * comprobante.tipo_de_cambio_pago
                comprobante.total_impuestos_trasladados = comprobante.total_impuestos_trasladados * comprobante.tipo_de_cambio_pago
                comprobante.total_impuestos_retenidos = comprobante.total_impuestos_retenidos * comprobante.tipo_de_cambio_pago

                lista_comprobantes.append(comprobante)

            SatComprobanteImpuestos.objects.bulk_update(lista_comprobantes, ['descuento','subtotal','total','base','iva_trasladado_importe','iva_retenido_importe','isr_retenido_importe','total_impuestos_trasladados','total_impuestos_retenidos','fecha_pago','forma_de_pago','referencia_pago','tipo_de_cambio_pago'])

    else:   
        print("Error")
        print(response.status_code)

    

    # Captura el tiempo final
    end_time = time.time()

    # Calcula el tiempo transcurrido
    elapsed_time = end_time - start_time
    print(f"Tiempo transcurrido: {elapsed_time:.4f} segundos")
    elapsed_time_minutes = elapsed_time / 60
    print(f"Tiempo transcurrido: {elapsed_time_minutes:.4f} minutos")


def get_referencias_emitidos(emisor,fecha_inicial,fecha_final):
    # Captura el tiempo inicial
    start_time = time.time()        
    comprobantes = SatComprobanteImpuestos.objects.filter(emisor=emisor, fecha__date__range=[fecha_inicial,fecha_final])
    df_comprobantes = pd.DataFrame(list(comprobantes.values('uuid','receptor','emisor','fecha','total','comprobante')))
    url = os.getenv('URL_API_CXC')

    params = {
            "fecha_inicial": fecha_inicial,
            "fecha_final": fecha_final,       
        }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if len(data['data']) > 0:
            df = pd.DataFrame(data['data'])
            df_new = df.merge(df_comprobantes, on=['uuid'])

            dict = df_new.to_dict(orient='records')
            lista_comprobantes = []
            for item in dict:
                comprobante = SatComprobanteImpuestos.objects.get(comprobante=item['comprobante'])
                comprobante.fecha_pago = item['fecha_aplicacion']
                comprobante.forma_de_pago = item['forma_de_pago']
                comprobante.referencia_pago = item['referencia']
                comprobante.sucursal = item['sucursal']
                comprobante.tipo_documento = item['tipo']

                comprobante.tipo_de_cambio_pago = Decimal(item['tipo_de_cambio_cobro'])
        
                comprobante.descuento = comprobante.descuento * comprobante.tipo_de_cambio_pago
                comprobante.subtotal = comprobante.subtotal * comprobante.tipo_de_cambio_pago
                comprobante.total = comprobante.total * comprobante.tipo_de_cambio_pago
                comprobante.base = comprobante.base * comprobante.tipo_de_cambio_pago
                comprobante.iva_trasladado_importe = comprobante.iva_trasladado_importe * comprobante.tipo_de_cambio_pago
                comprobante.iva_retenido_importe = comprobante.iva_retenido_importe * comprobante.tipo_de_cambio_pago
                comprobante.isr_retenido_importe = comprobante.isr_retenido_importe * comprobante.tipo_de_cambio_pago
                comprobante.total_impuestos_trasladados = comprobante.total_impuestos_trasladados * comprobante.tipo_de_cambio_pago
                comprobante.total_impuestos_retenidos = comprobante.total_impuestos_retenidos * comprobante.tipo_de_cambio_pago
                lista_comprobantes.append(comprobante)

            SatComprobanteImpuestos.objects.bulk_update(lista_comprobantes, ['descuento','subtotal','total','base','iva_trasladado_importe','iva_retenido_importe','isr_retenido_importe','total_impuestos_trasladados','total_impuestos_retenidos','fecha_pago','forma_de_pago','referencia_pago','sucursal','tipo_documento'])
    else:   
        print("Error")
        print(response.status_code)


   

    # Captura el tiempo final
    end_time = time.time()
    # Calcula el tiempo transcurrido
    elapsed_time = end_time - start_time
    print(f"Tiempo transcurrido: {elapsed_time:.4f} segundos")
    elapsed_time_minutes = elapsed_time / 60
    print(f"Tiempo transcurrido: {elapsed_time_minutes:.4f} minutos")
    

