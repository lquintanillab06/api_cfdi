from lxml import etree as ET
import datetime


from fpdf import FPDF
from fpdf.template import FlexTemplate, Template

from applications.commons.utils.importeALetra import  ImporteALetra
import qrcode
from tempfile import TemporaryFile, NamedTemporaryFile
from io import BytesIO


def get_cadena_original(xml):
    cadena = ""
    try:
        root = ET.fromstring(xml)  
        xsltfile = "applications/cfdi/cfdi_sat/xslt/xslt4/cadenaoriginal.xslt"
        xslt = ET.parse(xsltfile)
        transformer = ET.XSLT(xslt)
        cadena = transformer(root)
        return cadena
    except Exception as e:
        print(e)
        return cadena
    
def get_cadena_original_tfd(tfd):
    cadena_original = "|".join([
        "|",
        tfd['Version'],
        tfd['UUID'],
        tfd['FechaTimbrado'],
        tfd['RfcProvCertif'],
        tfd['SelloCFD'],
        tfd['NoCertificadoSAT'],
        "|"
    ])

    return cadena_original


class PDF(FPDF):

    def __init__(self, orientation = 'P', unit= 'mm', format= 'Letter', emisor = None, receptor = None, comprobante = None, timbrado = None):
        super().__init__(orientation, unit, format)
        self.coord_x = 10
        self.width_detail = 0 
        self.orientation = orientation
        self.emisor = emisor
        self.receptor = receptor
        self.comprobante = comprobante
        self.timbrado = timbrado

      # Page header
    def header(self):

        self.set_font('Times', 'B', 7)        
       #CUADRO NUMERO 1 
        self.rect(x=1,y=1,w=8.5,h=3.55)

        #1
        self.set_text_color(r= 0, g= 0, b = 0)
        self.cell(w=8.5,h=0.35,txt=f"{self.emisor['Nombre']}",align = "C", fill = 0, border=1)
        self.set_fill_color(r=192 , g= 192, b = 192)
        self.set_text_color(r= 255, g= 255, b = 255)
        self.cell(w=8.5,h=0.35,txt="FOLIO FISCAL (UUID)",align = "C", fill = 1,border = 1)
        self.cell(w=2.5,h=0.35,txt="SERIE Y FOLIO",align = "C", fill = 1,border = 1,ln=1)
        self.set_text_color(r= 0, g= 0, b = 0)
        self.cell(w=8.5,h=0.35,txt="",align = "C", fill = 0, border=0)
        self.cell(w=8.5,h=0.35,txt=f"{self.timbrado['UUID']}",align = "C", fill = 0)
        self.cell(w=2.5,h=0.35,txt=f"'{self.comprobante['Serie'] if 'Serie' in self.comprobante  else ''} - {self.comprobante['Folio'] if 'Folio' in self.comprobante else ''}",align = "C", fill = 0, ln=1,border="R")

        #2
        self.cell(w=8.5,h=0.35,txt="",align = "C", fill = 0)
        self.set_fill_color(r=192 , g= 192, b = 192)
        self.set_text_color(r= 255, g= 255, b = 255)
        self.cell(w=3.5,h=0.35,txt="FORMA PAGO",align = "C", fill = 1,border = 1)
        self.cell(w=3.5,h=0.35,txt="METODO PAGO",align = "C", fill = 1,border = 1)
        self.cell(w=4,h=0.35,txt="CONDICIONES PAGO",align = "C", fill = 1,border = 1,ln=1)
        self.cell(w=8.5,h=0.35,txt="",align = "C", fill = 0)
        self.set_fill_color(r=192 , g= 192, b = 192)
        self.set_text_color(r= 0, g= 0, b = 0)
        if 'FormaPago' in self.comprobante:
            self.cell(w=3.5,h=0.35,txt=f"{self.comprobante['FormaPago']}",align = "C", fill = 0)

        if 'MetodoPago' not in self.comprobante:
            self.comprobante['MetodoPago'] = ""        
        self.cell(w=3.5,h=0.35,txt=f"{self.comprobante['MetodoPago']}",align = "C", fill = 0)
        valorCP=""
        if 'CondicionesDePago' not in self.comprobante:
            valorCP = ""
        else:
            valorCP = self.comprobante['CondicionesDePago']
        self.cell(w=4,h=0.35,txt=f"{valorCP}",align = "C", fill = 0,border="R",ln=1)

        #3
        self.cell(w=8.5,h=0.35,txt="",align = "C", fill = 0)
        self.set_fill_color(r=192 , g= 192, b = 192)
        self.set_text_color(r= 255, g= 255, b = 255)
        self.cell(w=11,h=0.35,txt="RECEPTOR",align = "C", fill = 1,border = 1,ln=1)

        self.cell(w=8.5,h=0.35,txt="",align = "C", fill = 0)
        self.set_fill_color(r=192 , g= 192, b = 192)
        self.set_text_color(r= 0, g= 0, b = 0)
        self.set_font('Times', 'B', 8)
        self.multi_cell(w=11,h=0.4,txt=f"{self.receptor['Nombre']} \n      R.F.C.: {self.receptor['Rfc']}              USO CFDI: {self.receptor['UsoCFDI']}"
        ,align = "C", fill = 0,border=0)
        self.rect(x=9.5,y=2.75,w=11,h=1.8)
        self.set_font('Times', 'B', 8)
        self.ln(1)

        # DATOS DEL EMISOR 
        self.set_text_color(r= 0, g= 0, b = 0)

        # Espacio para el logo

        self.set_font('Times', 'B', 8)
        self.text(x=1.1,y=3.55,txt=f"R.F.C: {self.emisor['Rfc']}")
        self.text(x=1.1,y=3.95,txt=f"REGIMEN FISCAL: {self.emisor['RegimenFiscal']}")
        self.text(x=4.8,y=3.95,txt=f"EXPEDIDO EN: {self.comprobante['LugarExpedicion']}")
        self.text(x=1.1,y=4.35,txt=f"Ver.CFDI: {self.comprobante['Version']}")
        self.text(x=3.8,y=4.35,txt=f"FECHA: {self.comprobante['Fecha']}")
    
        self.set_text_color(r= 255, g= 255, b = 255)
        self.set_font('Times', 'B', 7)
        self.cell(w=3,h=0.35,txt="No.IDENTIFICACION",align = "C", fill = 1, border = 1)
        self.cell(w=1.55,h=0.35,txt="CANTIDAD",align = "C", fill = 1, border = 1)
        self.cell(w=2.3,h=0.35,txt="UNIDAD CLAVE",align = "C", fill = 1, border = 1)
        self.cell(w=7.7,h=0.35,txt="DESCRIPCION",align = "C", fill = 1, border = 1)
        self.cell(w=2.5,h=0.35,txt="PRECIO UNIT",align = "C", fill = 1, border = 1)
        self.cell(w=2.45,h=0.35,txt="IMPORTE",align = "C", fill = 1, border = 1,new_x="LMARGIN", new_y="NEXT",)
        self.set_text_color(r= 0, g= 0, b = 0)


    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-6)
        # Arial italic 8
        self.set_font('Arial', 'BI', 7)
        # Page number
        self.cell(0, 10, 'ESTE DOCUMENTO ES UNA REPRESENTACION DE UN CFDI    Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def print_pdf(xml):
    xml = xml.encode('utf-8')
    root = ET.fromstring(xml)  
    namespaces = {
                    "cfdi": "http://www.sat.gob.mx/cfd/4",
                    "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital"
                }
    
    cadena = get_cadena_original(xml)
    comprobante = root.attrib
    receptor = root.find('cfdi:Receptor',namespaces).attrib
    emisor = root.find('cfdi:Emisor',namespaces).attrib
    #concepto = root.find('.//cfdi:Concepto', namespaces).attrib
    conceptos = root.findall('.//cfdi:Concepto', namespaces)
    traslado_nodo = root.xpath('.//cfdi:Traslado', namespaces=namespaces)
    if len(traslado_nodo) > 0:
        traslado = traslado_nodo[0].attrib

    #retencion = root.find('.//cfdi:Retencion', namespaces).attrib
    impuestos_nodo = root.xpath('./cfdi:Impuestos', namespaces = namespaces)
    impuestos = {}
    if len(impuestos_nodo) > 0:
        impuestos = impuestos_nodo[0].attrib
    timbrado = root.find('.//tfd:TimbreFiscalDigital', namespaces).attrib



    pdf = PDF('P','cm','Letter',emisor=emisor,receptor=receptor,comprobante=comprobante,timbrado=timbrado)

    pdf.alias_nb_pages()
    pdf.add_page()  
    pdf.set_font('Times', 'B', 7)

    #PRIMERA TABLA 
   

    for concepto in conceptos:
        pdf.set_font('Times', '', 7)
        if 'NoIdentificacion' not in concepto.attrib:
            concepto.attrib['NoIdentificacion'] = ""
        pdf.cell(w=3,h=0.35,txt=f"{concepto.attrib['NoIdentificacion']}",align = "L", fill = 0, border = 1)
        pdf.cell(w=1.55,h=0.35,txt=f"{concepto.attrib['Cantidad']}",align = "C", fill = 0, border = 1)
        pdf.cell(w=2.3,h=0.35,txt=f"{concepto.attrib['ClaveUnidad']}",align = "L", fill = 0, border = 1)
        pdf.cell(w=7.7,h=0.35,txt=f"{concepto.attrib['Descripcion']}",align = "L", fill = 0, border = 1)
        pdf.cell(w=2.5,h=0.35,txt=f"{float(concepto.attrib['ValorUnitario'])}",align = "C", fill = 0, border = 1)
        pdf.cell(w=2.45,h=0.35,txt=f"{float(concepto.attrib['Importe'])}",align = "C", fill = 0, border = 1,new_x="LMARGIN", new_y="NEXT",)
        pdf.set_text_color(r= 0, g= 0, b = 0)
        pdf.set_fill_color(r=192 , g= 192, b = 192)
        pdf.set_text_color(r= 0, g= 0, b = 0)
        pdf.set_font('Times', 'B', 5)
        pdf.cell(w=0.8,h=0.22,txt="",align = "C", fill = 0, border = 0)
        pdf.cell(w=1.4,h=0.22,txt="CveProdSAT",align = "C", fill = 0, border = 1)
        pdf.cell(w=1.9,h=0.22,txt="Unidad SAT",align = "C", fill = 0, border = 1)
        pdf.cell(w=1.9,h=0.22,txt="Descto",align = "C", fill = 0, border = 1)
        pdf.cell(w=1.9,h=0.22,txt="Impuesto",align = "C", fill = 0, border = 1)
        pdf.cell(w=1.9,h=0.22,txt="TipoFactor",align = "C", fill = 0, border = 1)
        pdf.cell(w=1.9,h=0.22,txt="TasaOCuota",align = "C", fill = 0, border = 1)
        pdf.cell(w=1.9,h=0.22,txt="Base",align = "C", fill = 0, border = 1)
        pdf.cell(w=1.9,h=0.22,txt="ImprteIva",align = "C", fill = 0, border = 1,ln=1, new_x="LMARGIN", new_y="NEXT",)
        pdf.set_text_color(r= 0, g= 0, b = 0)
        pdf.set_font('Times', '', 5)
        pdf.cell(w=0.8,h=0.22,txt="",align = "C", fill = 0, border = 0,)
        pdf.cell(w=1.4,h=0.22,txt=f"{concepto.attrib['ClaveProdServ']}",align = "C", fill = 0,border = 1)
        if 'Unidad' not in concepto.attrib:
            concepto.attrib['Unidad'] = ""
        pdf.cell(w=1.9,h=0.22,txt=f"{concepto.attrib['Unidad']}",align = "C", fill = 0,border = 1)
        if 'Descuento' not in concepto.attrib:
            concepto.attrib['Descuento'] = "0.00"
        pdf.cell(w=1.9,h=0.22,txt=f"{concepto.attrib['Descuento']}",align = "C", fill = 0,border = 1 )
        #pdf.ln(0.3)
        if concepto.attrib['ObjetoImp'] == "02":
            pdf.cell(w=1.9,h=0.22,txt=f"{traslado['Impuesto']}",align = "C", fill = 0,border = 1)
            pdf.cell(w=1.9,h=0.22,txt=f"{traslado['TipoFactor']}",align = "C", fill = 0,border = 1)
            if 'TasaOCuota' not in traslado:
                traslado['TasaOCuota'] = "0.00"
            pdf.cell(w=1.9,h=0.22,txt=f"{traslado['TasaOCuota']}",align = "C", fill = 0,border = 1)
            pdf.cell(w=1.9,h=0.22,txt=f"{float(traslado['Base'])}",align = "C", fill = 0,border = 1)
            if 'Importe' not in traslado:
                traslado['Importe'] = "0.00"
            pdf.cell(w=1.9,h=0.22,txt=f"{traslado['Importe']}",align = "C", fill = 0,border = 1 ,new_x="LMARGIN", new_y="NEXT") 
        else: 
            pdf.cell(w=1.9,h=0.22,txt=f"",align = "C", fill = 0,border = 1 ,new_x="LMARGIN", new_y="NEXT") 

    #TOTALES
    pdf.ln(0.52)
    pdf.set_text_color(r= 0, g= 0, b = 0)
    pdf.set_font('Times', 'B', 7)
    pdf.cell(w=12.5,h=0.35,txt="IMPORTE CON LETRA",align = "L", fill = 0)
    pdf.cell(w=5,h=0.35,txt="SUBTOTAL",align = "R", fill = 0, )
    pdf.set_font('Times', '', 7)
    pdf.cell(w=2,h=0.35,txt=f"{float(comprobante['SubTotal'])}",align = "R", fill = 0, ln=1)

    pdf.cell(w=15.5,h=0.55,txt=f"{(ImporteALetra.convertirALetras(float(comprobante['Total'])))}",align = "L", fill = 0, border = 1)
    pdf.set_font('Times', 'B', 7)
    pdf.cell(w=2,h=0.35,txt="DESCUENTO",align = "R", fill = 0, border = 0 )
    pdf.set_font('Times', '', 7)

    sbt = float(comprobante['SubTotal'])
    ivaT = float(impuestos['TotalImpuestosTrasladados'] if 'TotalImpuestosTrasladados' in impuestos else 0)
    sbTtl = round(float(sbt + ivaT))

    pdf.cell(w=12.5,h=0.35,txt="",align = "L", fill = 0, )
    pdf.set_font('Times', 'B', 7)
    pdf.cell(w=5,h=0.35,txt="SUBTOTAL 1",align = "R", fill = 0,)
    pdf.set_font('Times', '', 7)
    pdf.cell(w=2,h=0.35,txt=f"{sbTtl}",align = "R", fill = 0,ln=1)

    pdf.cell(w=12.5,h=0.35,txt="",align = "L", fill = 0, )
    pdf.set_font('Times', 'B', 7)
    pdf.cell(w=5,h=0.35,txt="I.V.A. 16%",align = "R", fill = 0,)
    pdf.set_font('Times', '', 7)
    pdf.cell(w=2,h=0.35,txt=f"{impuestos['TotalImpuestosTrasladados'] if 'TotalImpuestosTrasladados' in impuestos else 0}",align = "R", fill = 0, ln=1)
    pdf.cell(w=12.5,h=0.35,txt="",align = "L", fill = 0)
    pdf.set_font('Times', 'B', 7)
    pdf.cell(w=5,h=0.35,txt="TOTAL",align = "R", fill = 0)
    pdf.set_font('Times', '', 7)
    pdf.cell(w=2,h=0.35,txt=f"{comprobante['Total']}",align = "R", fill = 0,ln=1)

    

    # Construyendo los datos del timbrado
 
    altura_disponible = pdf.h - pdf.get_y()
    if altura_disponible < 7:
        pdf.add_page()
        
    # Creando el archivo QR

    fin_sello = comprobante['Sello'][-8:]
    url_qr = f"""https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx?id={timbrado['UUID']}&re={emisor['Rfc']}&rr={receptor['Rfc']}&tt={comprobante['Total']}&fe={fin_sello}"""
    fp = TemporaryFile() 
    img = qrcode.make(url_qr)
    imgByteArr = BytesIO()
    img.save(imgByteArr, format='JPEG')
    fp.write(imgByteArr.getvalue())
    fp.seek(0) 
    #print(fp)

    # Agregando la imagen QR al pdf
    pdf.image(fp,  x=1, y= pdf.get_y(), w=3.5)
    fp.close() 
    
    
    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 8)
    pdf.cell(w=4,h=0.35,txt="R.F.C. PROV. CERTIF :",align = "L")
    pdf.set_font('Times', '', 8)
    pdf.cell(w=12,h=0.35,txt=f"{timbrado['RfcProvCertif']}",align = "L", new_y='NEXT') 

    pdf.set_x(5)
    pdf.set_font('Times', 'B', 8)
    pdf.cell(w=4,h=0.35,txt="TIPO DOCUMENTO :",align = "L")
    pdf.set_font('Times', '', 8)
    if (comprobante['TipoDeComprobante'] == "I"):
        pdf.cell(w=12,h=0.35,txt=f"INGRESO",align = "L", new_y='NEXT') 
    else:
        pdf.cell(w=12,h=0.35,txt=f"{comprobante['TipoDeComprobante']}",align = "L", new_y='NEXT') 
    
    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 8)
    pdf.cell(w=4,h=0.35,txt="FECHA TIMBRADO :",align = "L")
    pdf.set_font('Times', '', 8)
    pdf.cell(w=12,h=0.35,txt=f"{timbrado['FechaTimbrado']}",align = "L", new_y='NEXT') 

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 8)
    pdf.cell(w=4,h=0.35,txt="CERTIFICADO SAT :",align = "L")
    pdf.set_font('Times', '', 8)
    pdf.cell(w=12,h=0.35,txt=f"{timbrado['NoCertificadoSAT']}",align = "L", new_y='NEXT') 

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 8)
    pdf.cell(w=4,h=0.35,txt="CERTIFICADO EMISOR :",align = "L")
    pdf.set_font('Times', '', 8)
    pdf.cell(w=12,h=0.35,txt=f"{comprobante['NoCertificado']}",align = "L", new_y='NEXT') 

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 8)
    pdf.cell(w=4,h=0.35,txt="SELLO DIGITAL DEL CFDI :",align = "L")
    pdf.set_font('Times', '', 4.5)
    pdf.multi_cell(w=11,h=0.35,txt=f"{timbrado['SelloCFD']}",align = "L", new_y='NEXT') 

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 8)
    pdf.cell(w=4,h=0.35,txt="SELLO DIGITAL DEL SAT :",align = "L")
    pdf.set_font('Times', '', 4.5)
    pdf.multi_cell(w=11,h=0.35,txt=f"{timbrado['SelloSAT']}",align = "L", new_y='NEXT',new_x="LMARGIN") 

    pdf.set_font('Times', 'B', 10)
    pdf.cell(w=5,h=0.55,txt="CADENA ORIGINAL DEL COMPLEMENTO DE CERTIFICACION DIGITAL DEL SAT:",ln=1)
    pdf.set_font('Times', '', 5)
    pdf.multi_cell(w=19.5,h=0.35,txt=f"{get_cadena_original_tfd(timbrado)}",
    border=1,align="L")

    reporte = bytes(pdf.output())
    return reporte



def  print_acuse(acuse, xml):

    xml = xml.encode('utf-8')
    root = ET.fromstring(xml)  
    namespaces = {
                    "cfdi": "http://www.sat.gob.mx/cfd/4",
                    "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital"
                }
    
    comprobante = root.attrib
    receptor = root.find('cfdi:Receptor',namespaces).attrib
    emisor = root.find('cfdi:Emisor',namespaces).attrib
    timbrado = root.find('.//tfd:TimbreFiscalDigital', namespaces).attrib

    pdf = FPDF('P','cm','Letter')
    pdf.alias_nb_pages()
    pdf.add_page()  
    pdf.set_font('Times', 'B', 15)
    pdf.cell(w=20,h=0.55,txt="Acuse de Validacion SAT CFDI",ln=1, align="C")
    pdf.ln(1)

    fin_sello = comprobante['Sello'][-8:]
    url_qr = f"""https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx?id={timbrado['UUID']}&re={emisor['Rfc']}&rr={receptor['Rfc']}&tt={comprobante['Total']}&fe={fin_sello}"""
    fp = TemporaryFile() 
    img = qrcode.make(url_qr)
    imgByteArr = BytesIO()
    img.save(imgByteArr, format='JPEG')
    fp.write(imgByteArr.getvalue())
    fp.seek(0) 
    #print(fp)

    # Agregando la imagen QR al pdf
    pdf.image(fp,  x=1, y= pdf.get_y(), w=3.5)
    fp.close() 

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 11)
    pdf.cell(w=4.3,h=0.35,txt="UUID :",align = "L")
    pdf.set_font('Times', '', 11)
    pdf.cell(w=12,h=0.35,txt=f"{acuse['uuid']}",align = "L", new_y='NEXT') 
    pdf.ln(0.2)

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 11)
    pdf.cell(w=4.3,h=0.35,txt="EMISOR :",align = "L")
    pdf.set_font('Times', '', 11)
    pdf.cell(w=12,h=0.35,txt=f"{acuse['emisor']}",align = "L", new_y='NEXT') 
    pdf.ln(0.2)

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 11)
    pdf.cell(w=4.3,h=0.35,txt="RECEPTOR :",align = "L")
    pdf.set_font('Times', '', 11)
    pdf.cell(w=12,h=0.35,txt=f"{acuse['receptor']}",align = "L", new_y='NEXT') 
    pdf.ln(0.2)

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 11)
    pdf.cell(w=4.3,h=0.35,txt="TOTAL :",align = "L")
    pdf.set_font('Times', '', 11)
    pdf.cell(w=12,h=0.35,txt=f"{acuse['total']}",align = "L", new_y='NEXT') 
    pdf.ln(0.2)

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 11)
    pdf.cell(w=4.3,h=0.35,txt="FECHA :",align = "L")
    pdf.set_font('Times', '', 11)
    pdf.cell(w=12,h=0.35,txt=f"{acuse['fecha']}",align = "L", new_y='NEXT') 
    pdf.ln(0.2)

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 11)
    pdf.cell(w=4.3,h=0.35,txt="CANCELABLE :",align = "L")
    pdf.set_font('Times', '', 11)
    pdf.cell(w=12,h=0.35,txt=f"{acuse['es_cancelable']}",align = "L", new_y='NEXT') 
    pdf.ln(0.2)

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 11)
    pdf.cell(w=4.3,h=0.35,txt="ESTADO :",align = "L")
    pdf.set_font('Times', '', 11)
    pdf.cell(w=12,h=0.35,txt=f"{acuse['estado']}",align = "L", new_y='NEXT') 
    pdf.ln(0.2)

    pdf.set_x(5)
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Times', 'B', 11)
    pdf.cell(w=4.3,h=0.35,txt="FECHA VALIDACION :",align = "L")
    pdf.set_font('Times', '', 11)
    pdf.cell(w=12,h=0.35,txt=f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",align = "L", new_y='NEXT') 
    pdf.ln(0.2)

    reporte = bytes(pdf.output())
    return reporte
