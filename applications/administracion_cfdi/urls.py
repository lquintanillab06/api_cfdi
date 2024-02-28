from django.urls import path
from . import views


urlpatterns = [
    path('admin_cfdi/cargar_xml_solicitud', views.cargar_xmls_solicitud, name='cargar_xml_solicitud'),
    path('admin_cfdi/comprobantes_fiscales_recibidos', views.ComprobantesFiscalesRecibidosView.as_view(), name='comprobantes_fiscales'),
    path('admin_cfdi/comprobantes_fiscales_emitidos', views.ComprobantesFiscalesEmitidosView.as_view(), name='comprobantes_fiscales'),
    path('admin_cfdi/descargar_archivo_xml', views.descargar_archivo_xml, name='descargar_archivo_xml'),
    path('admin_cfid/imprimir_pdf', views.imprimir_pdf, name='imprimir_pdf'),
    path('admin_cfdi/exportar_csv', views.exportar_csv, name='exportar_csv'),
    path('admin_cfdi/validar_comprobante', views.validar_comprobante, name='validar_comprobante'),
]