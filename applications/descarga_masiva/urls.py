from django.urls import path
from . import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'codigo_respuesta', views.CodigoRespuestaViewset, basename='codigo_respuesta')

urlpatterns = [
    path('solicitud_descarga_masiva/', views.solicitud_descarga_masiva, name='solicitud_descarga_masiva' ),
    path('descarga_masiva_verificacion/', views.descarga_masiva_verificacion, name='descarga_masiva_verificacion' ),
    path('descargar_archivo_cfdi/', views.descargar_archivo, name='descargar_archivo_cfdi' ),
    path('solicitudes_por_contribuyente', views.SolicitudesPorContribuyente.as_view(), name='solicitudes_por_contribuyente' ),
    path('get_descarga_solicitud/', views.get_descarga_solicitud, name='get_descarga_solicitud' ),
    path('solicitud_descarga_cancelados/', views.solicitar_descarga_cancelados, name='solicitud_descarga_cancelados' ),
]

urlpatterns += router.urls