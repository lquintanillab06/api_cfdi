from django.urls import path
from . import views


urlpatterns = [
    path('buscador_cfdi', views.buscador_cfdi, name='buscador_cfdi'),
]
