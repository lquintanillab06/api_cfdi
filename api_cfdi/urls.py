
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('applications.knzl.urls')),
    path('api/',include('applications.cfdi.urls')),
    path('api/',include('applications.descarga_masiva.urls')),
    path('api/',include('applications.authentication.urls')),
    path('api/',include('applications.commons.urls')),
    path('api/',include('applications.administracion_cfdi.urls')),
    path('api/',include('applications.descarga_masiva_retenciones.urls')),
    path('api/',include('applications.buscador_cfdi.urls')),
]
