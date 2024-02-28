from django.urls import path
from . import views 

urlpatterns = [
    path('solicitud_descarga_masiva_retenciones', views.solicitud_descarga_masiva_retenciones, name='descarga_masiva_retenciones'),
    path('descarga_masiva_verificacion_retenciones', views.descarga_masiva_verificacion_retenciones, name='descarga_masiva_verificacion_retenciones')
]

 