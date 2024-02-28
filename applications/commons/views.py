from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CodigosPostalesMX
from .serializers import CodigosPostalesSerializer

# Create your views here.
@api_view(['GET'])
def get_address_from_zipcode(request):
    """
    Get address from zipcode
    """
    print(request.query_params)
    addresess = CodigosPostalesMX.objects.filter(codigo=request.query_params.get('zip'))
    print(addresess)

    addresess_serialized = CodigosPostalesSerializer(addresess, many=True)

    return Response(addresess_serialized.data)
  