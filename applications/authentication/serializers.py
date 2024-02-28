from rest_framework import serializers
from .models import User 
from django.contrib.auth.models import Permission





class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Permission
        fields = ["id","codename"]


class UserSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many= True)
    #sucursal = SucursalSerializer()
    class Meta:
        model= User
        fields = ["nombre","nombres","username","user_permissions"]
       
