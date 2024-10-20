from lxml import etree as ET
from datetime import datetime


from fpdf import FPDF
from fpdf.template import FlexTemplate, Template

from applications.commons.utils.importeALetra import  ImporteALetra
import qrcode
from tempfile import TemporaryFile, NamedTemporaryFile
from io import BytesIO


''' def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename) '''


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
  

class PDF(FPDF):

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-6)
        # Arial italic 8
        self.set_font('Arial', 'BI', 7)
        # Page number
        self.cell(0, 10, 'ESTE DOCUMENTO ES UNA REPRESENTACION DE UN CFDI    Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def print_pdf(xml):
    # print(xml)
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

    pdf = PDF('P','cm','Letter')
    pdf.alias_nb_pages()
    pdf.add_page()  
    pdf.set_font('Times', 'B', 7)

    #CUADRO NUMERO 1 
    pdf.rect(x=1,y=1,w=8.5,h=3.55)
    #informacion de la parte numero 2
    #pdf.image('logo.png', x=4, y=1.2, w=7,h=2.0)
    #1
    pdf.set_text_color(r= 0, g= 0, b = 0)
    pdf.cell(w=8.5,h=0.35,txt=f"{emisor['Nombre']}",align = "C", fill = 0, border=1)
    pdf.set_fill_color(r=192 , g= 192, b = 192)
    pdf.set_text_color(r= 255, g= 255, b = 255)
    pdf.cell(w=8.5,h=0.35,txt="FOLIO FISCAL (UUID)",align = "C", fill = 1,border = 1)
    pdf.cell(w=2.5,h=0.35,txt="SERIE Y FOLIO",align = "C", fill = 1,border = 1,ln=1)
    pdf.set_text_color(r= 0, g= 0, b = 0)
    pdf.cell(w=8.5,h=0.35,txt="",align = "C", fill = 0, border=0)
    pdf.cell(w=8.5,h=0.35,txt=f"{timbrado['UUID']}",align = "C", fill = 0)

    pdf.cell(w=2.5,h=0.35,txt=f"'{comprobante['Serie'] if 'Serie' in comprobante  else ''} - {comprobante['Folio']}",align = "C", fill = 0, ln=1,border="R")

    #2
    pdf.cell(w=8.5,h=0.35,txt="",align = "C", fill = 0)
    pdf.set_fill_color(r=192 , g= 192, b = 192)
    pdf.set_text_color(r= 255, g= 255, b = 255)
    pdf.cell(w=3.5,h=0.35,txt="FORMA PAGO",align = "C", fill = 1,border = 1)
    pdf.cell(w=3.5,h=0.35,txt="METODO PAGO",align = "C", fill = 1,border = 1)
    pdf.cell(w=4,h=0.35,txt="CONDICIONES PAGO",align = "C", fill = 1,border = 1,ln=1)

    pdf.cell(w=8.5,h=0.35,txt="",align = "C", fill = 0)
    pdf.set_fill_color(r=192 , g= 192, b = 192)
    pdf.set_text_color(r= 0, g= 0, b = 0)
    if 'FormaPago' in comprobante:
        pdf.cell(w=3.5,h=0.35,txt=f"{comprobante['FormaPago']}",align = "C", fill = 0)
    pdf.cell(w=3.5,h=0.35,txt=f"{comprobante['MetodoPago']}",align = "C", fill = 0)
    valorCP=""
    if 'CondicionesDePago' not in comprobante:
        valorCP = ""
    else:
        valorCP = comprobante['CondicionesDePago']
    pdf.cell(w=4,h=0.35,txt=f"{valorCP}",align = "C", fill = 0,border="R",ln=1)

    #3
    pdf.cell(w=8.5,h=0.35,txt="",align = "C", fill = 0)
    pdf.set_fill_color(r=192 , g= 192, b = 192)
    pdf.set_text_color(r= 255, g= 255, b = 255)
    pdf.cell(w=11,h=0.35,txt="RECEPTOR",align = "C", fill = 1,border = 1,ln=1)

    pdf.cell(w=8.5,h=0.35,txt="",align = "C", fill = 0)
    pdf.set_fill_color(r=192 , g= 192, b = 192)
    pdf.set_text_color(r= 0, g= 0, b = 0)
    pdf.set_font('Times', 'B', 8)
    pdf.multi_cell(w=11,h=0.4,txt=f"{receptor['Nombre']} \n      R.F.C.: {receptor['Rfc']}              USO CFDI: {receptor['UsoCFDI']}"
    ,align = "C", fill = 0,border=0)
    pdf.rect(x=9.5,y=2.75,w=11,h=1.8)


    pdf.set_font('Times', 'B', 8)
    pdf.ln(1)
    # pdf.cell(w=13,h=1,txt="RFC:",align = "L", fill = 0,ln=2)
    # pdf.cell(w=13,h=1,txt="Regimen Fiscal: ",align = "L", fill = 0,ln=3)
    # pdf.cell(w=13,h=1,txt="Lugar de Expedicion: ",align = "L", fill = 0,ln=4)
    # DATOS DEL EMISOR 
    pdf.set_text_color(r= 0, g= 0, b = 0)

    # Espacio para el logo

    #rr = emisor['Rfc']
    #abv = rr[0:4]
    #pdf.set_font('Times', 'B', 45)
    #pdf.text(x=3.3,y=2.8,txt=(f"{abv}"))
    pdf.set_font('Times', 'B', 8)
    #pdf.text(x=1.1,y=3.3,txt=f"PAPER IMPORTS S.A DE C.V")
    pdf.text(x=1.1,y=3.55,txt=f"R.F.C: {emisor['Rfc']}")
    pdf.text(x=1.1,y=3.95,txt=f"REGIMEN FISCAL: {emisor['RegimenFiscal']}")
    pdf.text(x=4.8,y=3.95,txt=f"EXPEDIDO EN: {comprobante['LugarExpedicion']}")
    pdf.text(x=1.1,y=4.35,txt=f"Ver.CFDI: {comprobante['Version']}")
    pdf.text(x=3.8,y=4.35,txt=f"FECHA: {comprobante['Fecha']}")


       #PRIMERA TABLA 
    pdf.set_text_color(r= 255, g= 255, b = 255)
    pdf.set_font('Times', 'B', 7)
    pdf.cell(w=3,h=0.35,txt="No.IDENTIFICACION",align = "C", fill = 1, border = 1)
    pdf.cell(w=1.55,h=0.35,txt="CANTIDAD",align = "C", fill = 1, border = 1)
    pdf.cell(w=2.3,h=0.35,txt="UNIDAD CLAVE",align = "C", fill = 1, border = 1)
    pdf.cell(w=7.7,h=0.35,txt="DESCRIPCION",align = "C", fill = 1, border = 1)
    pdf.cell(w=2.5,h=0.35,txt="PRECIO UNIT",align = "C", fill = 1, border = 1)
    pdf.cell(w=2.45,h=0.35,txt="IMPORTE",align = "C", fill = 1, border = 1,new_x="LMARGIN", new_y="NEXT",)
    pdf.set_text_color(r= 0, g= 0, b = 0)

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
        pdf.cell(w=0.8,h=0.22,txt="",align = "C", fill = 0, border = 0)
        pdf.cell(w=1.4,h=0.22,txt=f"{concepto.attrib['ClaveProdServ']}",align = "C", fill = 0,border = 1)
        pdf.cell(w=1.9,h=0.22,txt=f"{concepto.attrib['Unidad']}",align = "C", fill = 0,border = 1)
        if 'Descuento' not in concepto.attrib:
            concepto.attrib['Descuento'] = "0.00"
        pdf.cell(w=1.9,h=0.22,txt=f"{concepto.attrib['Descuento']}",align = "C", fill = 0,border = 1,new_x="LMARGIN", new_y="NEXT") 
        pdf.ln(0.3)
        ''' pdf.cell(w=1.9,h=0.22,txt=f"{traslado['Impuesto']}",align = "C", fill = 0,border = 1)
        pdf.cell(w=1.9,h=0.22,txt=f"{traslado['TipoFactor']}",align = "C", fill = 0,border = 1)
        pdf.cell(w=1.9,h=0.22,txt=f"{traslado['TasaOCuota']}",align = "C", fill = 0,border = 1)
        pdf.cell(w=1.9,h=0.22,txt=f"{float(traslado['Base'])}",align = "C", fill = 0,border = 1)
        pdf.cell(w=1.9,h=0.22,txt=f"{traslado['Importe']}",align = "C", fill = 0,border = 1) '''

 


    #TOTALES
    pdf.ln(0.52)
    pdf.set_text_color(r= 0, g= 0, b = 0)
    pdf.set_font('Times', 'B', 7)
    pdf.cell(w=12.5,h=0.35,txt="IMPORTE CON LETRA",align = "L", fill = 0)
    pdf.cell(w=5,h=0.35,txt="SUBTOTAL",align = "R", fill = 0, )
    pdf.set_font('Times', '', 7)
    pdf.cell(w=2,h=0.35,txt=f"{float(comprobante['SubTotal'])}",align = "R", fill = 0, ln=1)

    pdf.cell(w=15.5,h=0.55,txt=f"{(ImporteALetra.convertirALetras(float(comprobante['Total'])))}",align = "L", fill = 0, border = 1)
     #pdf.cell(w=15.5,h=0.55,txt=f"{(ImporteALetra.convertirALetras(19999999))}",align = "L", fill = 0, border = 1)
    pdf.set_font('Times', 'B', 7)
    pdf.cell(w=2,h=0.35,txt="DESCUENTO",align = "R", fill = 0, border = 0 )
    pdf.set_font('Times', '', 7)
    #pdf.cell(w=2,h=0.35,txt=f"{comprobante['Descuento']}",align = "R", fill = 0,ln=1)

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


    espacio = pdf.h - pdf.get_y()

    print(espacio)

    #pdf.cell(w=12.5,h=0.35,txt="",align = "L", fill = 0,)
    #pdf.set_font('Times', 'B', 7)
    #pdf.cell(w=5,h=0.35,txt="RETENCION",align = "R", fill = 0, )
    #pdf.set_font('Times', '', 7)
    #pdf.cell(w=2,h=0.35,txt=f"{impuestos['TotalImpuestosRetenidos']}",align = "R", fill = 0, ln=1)

    pdf.cell(w=12.5,h=0.35,txt="",align = "L", fill = 0)
    pdf.set_font('Times', 'B', 7)
    pdf.cell(w=5,h=0.35,txt="TOTAL",align = "R", fill = 0)
    pdf.set_font('Times', '', 7)
    pdf.cell(w=2,h=0.35,txt=f"{comprobante['Total']}",align = "R", fill = 0,ln=1)


 

    #CUADRO NUMERO 2
    pdf.set_auto_page_break(True, margin = 2)#5 y 2
 
    print(pdf.h)
    print(pdf.w)
    yy = pdf.get_y()
   

    print("*"*100)
    ancho_max = 100
    print((pdf.get_string_width(str(cadena))))
    print(type(str(cadena))) 
    print("*"*100)
    pdf.set_y(pdf.h - ((pdf.get_string_width(str(cadena))/30)))
    
  
    pdf.set_font('Times', 'B', 10)
    pdf.cell(w=5,h=0.55,txt="CADENA ORIGINAL DEL COMPLEMENTO DE CERTIFICACION DIGITAL DEL SAT:",ln=1)
    pdf.set_font('Times', '', 5)
    pdf.multi_cell(w=19.5,h=0.35,txt=f"{cadena}",
    #pdf.multi_cell(w=19.5,h=0.35,txt=f"Texto cadena",
    border=1,align="L")

    # Creando el archivo QR
    url_qr = f"""https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx?id={timbrado['UUID']}&re={emisor['Rfc']}&rr={receptor['Rfc']}&tt=0.00&fe=fK7wjA=="""
    fp = TemporaryFile() 
    img = qrcode.make(url_qr)
    imgByteArr = BytesIO()
    img.save(imgByteArr, format='JPEG')
    fp.write(imgByteArr.getvalue())
    fp.seek(0)
    #print(fp)

    # Agregando la imagen QR al pdf
    pdf.image(fp,  x=1, y=16, w=5)
    fp.close() 


    reporte = bytes(pdf.output())
    return reporte
    

