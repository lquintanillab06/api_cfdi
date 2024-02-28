from django.db import models


class ComprobanteFiscalManager(models.Manager):

    def get_emitidos(self, contribuyente, fecha_inicial, fecha_final):
        return self.filter(rfc_emisor=contribuyente.rfc, fecha__date__range=[fecha_inicial, fecha_final],contribuyente=contribuyente)
   
    def get_recibidos(self, contribuyente, fecha_inicial, fecha_final):
        return self.filter(rfc_receptor=contribuyente.rfc, fecha__date__range=[fecha_inicial, fecha_final], contribuyente=contribuyente)
    
    def get_emitidos_to_csv(self, contribuyente, fecha_inicial, fecha_final):
        return self.filter(rfc_emisor=contribuyente.rfc, contribuyente=contribuyente, fecha__date__range=[fecha_inicial, fecha_final])
    
    def get_recibidos_to_csv(self, contribuyente, fecha_inicial, fecha_final):
         return self.filter(rfc_receptor=contribuyente.rfc, contribuyente=contribuyente, fecha__date__range=[fecha_inicial, fecha_final])

    

