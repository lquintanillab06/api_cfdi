from django.urls import path
from . import views

url_certificado = [
    path("cfdi/get_key/<int:contribuyente_id>",views.get_key, name="get_key"),
    path("cfdi/get_cert/<int:contribuyente_id>",views.get_cert, name="get_cert"),
    path("cfdi/get_pfx/<int:contribuyente_id>",views.get_pfx, name="get_pfx"),
    path("cfdi/get_numero_certificado/<int:contribuyente_id>",views.get_numero_certificado, name="get_numero_certificado"),
    path("cfdi/set_numero_certificado/<int:contribuyente_id>",views.set_numero_certificado, name="set_numero_certificado"),
    path("cfdi/upload_cert/<int:contribuyente_id>/<filename>",views.UploadCertView.as_view(),name="upload_cert_view"),
    path("cfdi/upload_key/<int:contribuyente_id>/<filename>",views.UploadKeyView.as_view(),name="upload_key_view"),
    path("cfdi/upload_pfx/<int:contribuyente_id>/<filename>",views.UploadPfxView.as_view(),name="upload_pfx_view"),
    path("cfdi/upload_cert_firma/<int:contribuyente_id>/<filename>",views.UploadCertFirmaView.as_view(),name="upload_cert_firma"),
    path("cfdi/upload_key_firma/<int:contribuyente_id>/<filename>",views.UploadKeyFirmaView.as_view(),name="upload_key_firma"),
    path("cfdi/get_encrypted_key",views.get_encrypted_key, name="get_encrypted_key"),
    ]

url_contribuyente = [
    path('cfdi/contribuyente_create', views.ContribuyenteCreate.as_view(), name= 'contribuyente_create'),
    path('cfdi/contribuyente_retrieve/<pk>/', views.ContribuyenteDetailView.as_view(), name= 'contribuyente_retrieve'),
    path('cfdi/contribuyente_list',views.ContribuyenteList.as_view(), name='contribuyente_list'),
    path('cfdi/contribuyente_update/<pk>/',views.ContribuyenteGetUpdate.as_view(), name='contribuyente_update'),
    path('cfdi/contribuyente_encrypted_password',views.encrypted_password_contribuyente, name='contribuyente_encrypted_password'),
    path('cfdi/find_contribuyente',views.SearchContribuyente.as_view(), name='find_contribuyente'),
    ]

url_regimen_fiscal = [
    path('cfdi/regimen_fiscal_list',views.RegimenFiscalList.as_view(), name='regimen_fiscal_list'),
    path('cfdi/regimen_fiscal_create',views.RegimenFiscalCreate.as_view(), name='regimen_fiscal_create'),
    path('cfdi/regimen_fiscal_edit/<pk>/',views.RegimenFiscalUpdate.as_view(), name='regimen_fiscal_update'),
]

url_producto_sat = [
    path('cfdi/producto_sat_list',views.ProductoSatList.as_view(), name='producto_sat_list'),
    path('cfdi/producto_sat_create',views.ProductoSatCreate.as_view(), name='producto_sat_create'),
    path('cfdi/producto_sat_edit/<pk>/',views.ProductoSatUpdate.as_view(), name='producto_sat_update'),
]

url_unidad_sat = [
    path('cfdi/unidad_sat_list',views.UnidadSatList.as_view(), name='unidad_sat_list'),
    path('cfdi/unidad_sat_create',views.UnidadSatCreate.as_view(), name='unidad_sat_create'),
    path('cfdi/unidad_sat_edit/<pk>/',views.UnidadSatUpdate.as_view(), name='unidad_sat_update'),
]

url_uso_cfdi = [
    path('cfdi/uso_cfdi_list',views.UsoDeCfdiList.as_view(), name='uso_cfdi_list'),
    path('cfdi/uso_cfdi_create',views.UsoDeCfdiCreate.as_view(), name='uso_cfdi_create'),
    path('cfdi/uso_cfdi_edit/<pk>/',views.UsoDeCfdiUpdate.as_view(), name='uso_cfdi_update'),
    path('cfdi/uso_cfdi_get/<pk>/',views.UsoDeCfdiDetailView.as_view(), name='uso_cfdi_get'),
]

url_metodo_pago = [
    path('cfdi/metodo_pago_list',views.MetodoPagoList.as_view(), name='metodo_pago_list'),
    path('cfdi/metodo_pago_create',views.MetodoPagoCreate.as_view(), name='metodo_pago_create'),
    path('cfdi/metodo_pago_edit/<pk>/',views.MetodoPagoUpdate.as_view(), name='metodo_pago_update'),
]

url_tipo_comprobante = [
    path('cfdi/tipo_comprobante_list',views.TipoComprobanteList.as_view(), name='tipo_comprobante_list'),
    path('cfdi/tipo_comprobante_create',views.TipoComprobanteCreate.as_view(), name='tipo_comprobante_create'),
    path('cfdi/tipo_comprobante_edit/<pk>/',views.TipoComprobanteUpdate.as_view(), name='tipo_comprobante_update'),
]

url_forma_pago = [
    path('cfdi/forma_pago_list',views.FormaPagoList.as_view(), name='forma_pago_list'),
    path('cfdi/forma_pago_create',views.FormaPagoCreate.as_view(), name='forma_pago_create'),
    path('cfdi/forma_pago_edit/<pk>/',views.FormaPagoUpdate.as_view(), name='forma_pago_update'),
]

url_subtipo_comprobante = [
    path('cfdi/subtipo_comprobante_list',views.SubtipoComprobanteList.as_view(), name='subtipo_comprobante_list'),
    path('cfdi/subtipo_comprobante_create',views.SubtipoComprobanteCreate.as_view(), name='subtipo_comprobante_create'),
    path('cfdi/subtipo_comprobante_edit/<pk>/',views.SubtipoComprobanteUpdate.as_view(), name='subtipo_comprobante_update'),
]


urlpatterns = url_certificado + url_contribuyente + url_regimen_fiscal + url_producto_sat + url_unidad_sat + url_uso_cfdi + url_metodo_pago

urlpatterns = urlpatterns + url_tipo_comprobante + url_forma_pago + url_subtipo_comprobante