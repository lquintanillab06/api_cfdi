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
    path('admin_cfdi/verificar_cancelados', views.verificar_cancelados, name='verificar_cancelados'),
    path('admin_cfdi/imprimir_acuse', views.imprimir_acuse, name='imprimir_acuse'),
    path('admin_cfdi/generar_impuestos', views.generar_comprobante_impuestos, name='generar_impuestos'),
    path('admin_cfdi/get_referencias_pago', views.get_referencias_pago, name='get_referencias_pago'),
    path('admin_cfdi/sat_comprobantes_impuestos', views.get_sat_comprobantes_impuestos, name='sat_comprobantes_impuestos'),
    path('admin_cfdi/sat_comprobantes_impuestos_ppd', views.get_sat_comprobantes_impuestos_ppd, name='sat_comprobantes_impuestos_ppd'),
      path('admin_cfdi/exportar_impuestos_csv', views.exportar_impuestos_csv, name='exportar_impuestos_csv'),
]