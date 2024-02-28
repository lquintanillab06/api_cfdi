
import  lxml.etree as ET





class CadenaOriginalBuilder():

    def build_from_xml(self,xml):
        #print("Generando la cadena original")
        source = self.buildSource(xml)
        transformer = self.getTransformer()
        cadena = transformer(source)
        return cadena


    def buildSource_from_xml(self, xml):
        xmlSource = ET.XML( xml.replace('<?xml version="1.0" encoding="utf-8"?>', ''))
        return xmlSource

    def getTransformer(self):
        xsltfile = "applications/cfdi/cfdi_sat/xslt/xslt4/cadenaoriginal.xslt"
        xslt = ET.parse(xsltfile)
        transformer = ET.XSLT(xslt)
        return transformer


        
        

