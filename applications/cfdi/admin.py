from django.contrib import admin
from .models import RegimenFiscal, Contribuyente, UsoDeCfdi, MetodoPago, FormaPago, TipoComprobante, ProductoSat, UnidadSat, SubTipoComprobante

# Register your models here.

admin.site.register(RegimenFiscal)
admin.site.register(Contribuyente)
admin.site.register(UsoDeCfdi)
admin.site.register(MetodoPago)
admin.site.register(FormaPago)
admin.site.register(TipoComprobante)
admin.site.register(ProductoSat)
admin.site.register(UnidadSat)
admin.site.register(SubTipoComprobante)

