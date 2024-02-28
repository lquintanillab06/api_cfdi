from django.urls import path
from . import views

urlpatterns = [
   path('get_address_from_zipcode/', views.get_address_from_zipcode, name='get_address_from_zipcode' ), 
]