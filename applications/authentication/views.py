from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (RetrieveAPIView,)
from rest_framework.views import APIView
from .serializers import UserSerializer


# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Add extra responses here
        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def get_user(request):
    
    ''' print(request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1])
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    authentication = JWTAuthentication()
    token_validated = authentication.get_validated_token(token)
    print(token_validated) '''
    #user, _ = authentication.get_user(token_validated)
    #print(user)
    authentication = JWTAuthentication()
    header = authentication.get_header(request)
    raw_token = authentication.get_raw_token(header) 
    validated_token = authentication.get_validated_token(raw_token)
    user = authentication.get_user(validated_token)
    user_serialized = UserSerializer(user)
    return Response(user_serialized.data)


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def test(request):
    return Response({"message":"succesfully"})

class GetUser(APIView):
    serializer_class = UserSerializer

    def get(self, request):
      
        authentication = JWTAuthentication()
        header = authentication.get_header(self.request)
        raw_token = authentication.get_raw_token(header) 
        validated_token = authentication.get_validated_token(raw_token)
        user = authentication.get_user(validated_token)
        user_serialized = UserSerializer(user)
    
        return Response(user_serialized.data)