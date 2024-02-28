from django.db import models

class ContribuyenteManager(models.Manager):
    
    def find_contribuyente(self, term):
        founds = self.filter(razon_social__icontains=term, activo=True)
        return founds
