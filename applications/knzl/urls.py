from django.urls import path
from . import views 

urlpatterns = [
    path('knzl/', views.knzl_view, name='knzl' ),
    path('test/', views.knzl_command, name='test' ),
]