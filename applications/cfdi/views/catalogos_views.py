from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import (RetrieveAPIView, ListAPIView,CreateAPIView,DestroyAPIView,UpdateAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView)
from ..serializers import (ContribuyenteShowSerializer,RegimenFiscalSerializer,UsoDeCfdiSerializer,MetodoPagoSerializer,FormaPagoSerializer,TipoComprobanteSerializer,
                           ProductoSatSerializer,UnidadSatSerializer, ContribuyenteFormSerializer, SubTipoComprobanteSerializer, SubTipoComprobanteFormSerializer, UsoDeCfdiFormSerializer)
from ..models import (Contribuyente,RegimenFiscal,UsoDeCfdi,MetodoPago,FormaPago,TipoComprobante,ProductoSat,UnidadSat,SubTipoComprobante)
from ..services.encrypt_text import encrypt_text,generate_key

# Vistas para el catalogo de contribuyente

class ContribuyenteDetailView(RetrieveAPIView):
    serializer_class = ContribuyenteShowSerializer
    queryset = Contribuyente.objects.filter()

class ContribuyenteList(ListAPIView):
    queryset = Contribuyente.objects.all()
    serializer_class = ContribuyenteShowSerializer

class ContribuyenteCreate(CreateAPIView):
    serializer_class = ContribuyenteFormSerializer

class ContribuyenteDelete(DestroyAPIView):
    serializer_class = ContribuyenteShowSerializer
    queryset = Contribuyente.objects.filter()

class ContribuyenteUpdate(UpdateAPIView):
    serializer_class = ContribuyenteShowSerializer
    queryset = Contribuyente.objects.filter()

class ContribuyenteGetUpdate(RetrieveUpdateAPIView):
    serializer_class = ContribuyenteFormSerializer
    queryset = Contribuyente.objects.filter()

class ContribuyenteGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = ContribuyenteShowSerializer
    queryset = Contribuyente.objects.filter()

class SearchContribuyente(ListAPIView):
    serializer_class = ContribuyenteShowSerializer
    def get_queryset(self):
        print(self.request.query_params.get('razon_social'))
        term = self.request.query_params.get('razon_social')
        founds = Contribuyente.objects.find_contribuyente(term)
        return   founds
    
# Vistas para el catalogo de RegimenFiscal
    
class RegimenFiscalList(ListAPIView):
    queryset = RegimenFiscal.objects.all()
    serializer_class = RegimenFiscalSerializer

class RegimenFiscalDetailView(RetrieveAPIView):
    serializer_class = RegimenFiscalSerializer
    queryset = RegimenFiscal.objects.filter()

class RegimenFiscalGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = RegimenFiscalSerializer
    queryset = RegimenFiscal.objects.filter()

class RegimenFiscalUpdate(UpdateAPIView):
    serializer_class = RegimenFiscalSerializer
    queryset = RegimenFiscal.objects.filter()

class RegimenFiscalCreate(CreateAPIView):
    serializer_class = RegimenFiscalSerializer

#Vistas para el catalogo de UsoDeCfdi

class UsoDeCfdiList(ListAPIView):
    queryset = UsoDeCfdi.objects.all()
    serializer_class = UsoDeCfdiSerializer

class UsoDeCfdiDetailView(RetrieveAPIView):
    serializer_class = UsoDeCfdiSerializer
    queryset = UsoDeCfdi.objects.filter()

class UsoDeCfdiGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = UsoDeCfdiSerializer
    queryset = UsoDeCfdi.objects.filter()

class UsoDeCfdiUpdate(UpdateAPIView):
    serializer_class = UsoDeCfdiFormSerializer
    queryset = UsoDeCfdi.objects.filter()

class UsoDeCfdiCreate(CreateAPIView):
    serializer_class = UsoDeCfdiFormSerializer

#Vistas para el catalogo de MetodoPago


class MetodoPagoList(ListAPIView):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer

class MetodoPagoDetailView(RetrieveAPIView):
    serializer_class = MetodoPagoSerializer
    queryset = MetodoPago.objects.filter()

class MetodoPagoGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = MetodoPagoSerializer
    queryset = MetodoPago.objects.filter()

class MetodoPagoUpdate(UpdateAPIView):
    serializer_class = MetodoPagoSerializer
    queryset = MetodoPago.objects.filter()

class MetodoPagoCreate(CreateAPIView):
    serializer_class = MetodoPagoSerializer

#Vistas para el catalogo de FormaPago

class FormaPagoList(ListAPIView):
    queryset = FormaPago.objects.all()
    serializer_class = FormaPagoSerializer

class FormaPagoDetailView(RetrieveAPIView):
    serializer_class = FormaPagoSerializer
    queryset = FormaPago.objects.filter()

class FormaPagoGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = FormaPagoSerializer
    queryset = FormaPago.objects.filter()

class FormaPagoUpdate(UpdateAPIView):
    serializer_class = FormaPagoSerializer
    queryset = FormaPago.objects.filter()

class FormaPagoCreate(CreateAPIView):
    serializer_class = FormaPagoSerializer

#Vistas para el catalogo de TipoComprobante

class TipoComprobanteList(ListAPIView):
    queryset = TipoComprobante.objects.all()
    serializer_class = TipoComprobanteSerializer

class TipoComprobanteDetailView(RetrieveAPIView):
    serializer_class = TipoComprobanteSerializer
    queryset = TipoComprobante.objects.filter()

class TipoComprobanteGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = TipoComprobanteSerializer
    queryset = TipoComprobante.objects.filter()

class TipoComprobanteUpdate(UpdateAPIView):
    serializer_class = TipoComprobanteSerializer
    queryset = TipoComprobante.objects.filter()

class TipoComprobanteCreate(CreateAPIView):
    serializer_class = TipoComprobanteSerializer

# Vistas para el catalogo de SubtipoComprobante
class SubtipoComprobanteList(ListAPIView):
    queryset = SubTipoComprobante.objects.all()
    serializer_class = SubTipoComprobanteSerializer
    
class SubtipoComprobanteDetailView(RetrieveAPIView):
    serializer_class = SubTipoComprobanteSerializer
    queryset = SubTipoComprobante.objects.filter()

class SubtipoComprobanteGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = SubTipoComprobanteFormSerializer
    queryset = SubTipoComprobante.objects.filter()

class SubtipoComprobanteUpdate(UpdateAPIView):
    serializer_class = SubTipoComprobanteFormSerializer
    queryset = SubTipoComprobante.objects.filter()
  

class SubtipoComprobanteCreate(CreateAPIView):    
    serializer_class = SubTipoComprobanteFormSerializer



#Vistas para el catalogo de ProductoSat

class ProductoSatList(ListAPIView):
    queryset = ProductoSat.objects.all()
    serializer_class = ProductoSatSerializer

class ProductoSatDetailView(RetrieveAPIView):
    serializer_class = ProductoSatSerializer
    queryset = ProductoSat.objects.filter()

class ProductoSatGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductoSatSerializer
    queryset = ProductoSat.objects.filter()

class ProductoSatUpdate(UpdateAPIView):
    serializer_class = ProductoSatSerializer
    queryset = ProductoSat.objects.filter()

class ProductoSatCreate(CreateAPIView):
    serializer_class = ProductoSatSerializer

#Vistas para el catalogo de UnidadSat

class UnidadSatList(ListAPIView):
    queryset = UnidadSat.objects.all()
    serializer_class = UnidadSatSerializer

class UnidadSatDetailView(RetrieveAPIView):
    serializer_class = UnidadSatSerializer
    queryset = UnidadSat.objects.filter()

class UnidadSatGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = UnidadSatSerializer
    queryset = UnidadSat.objects.filter()

class UnidadSatUpdate(UpdateAPIView):
    serializer_class = UnidadSatSerializer
    queryset = UnidadSat.objects.filter()

class UnidadSatCreate(CreateAPIView):
    serializer_class = UnidadSatSerializer


# ViewSets


class ContribuyenteViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Contribuyente.objects.all()
        serializer = ContribuyenteShowSerializer(queryset,many= True)
        return Response(serializer.data)
    
    def create(self, request):
        print(request)
        return Response("Succesfully Create")
    
    def retrieve(self, request, pk=None):
        queryset = Contribuyente.objects.filter(pk=pk).first()
        print(queryset)
        serializer = ContribuyenteShowSerializer(queryset)
        return Response(serializer.data)
        
    def update(self, request, pk=None):
        print(request)
        return Response("Succesfully Update")

    def partial_update(self, request, pk=None):
        print(request)
        return Response("Succesfully Partial")

    def destroy(self, request, pk=None):
        print(request)
        return Response("Succesfully")


    
@api_view(['POST'])
def encrypted_password_contribuyente(request):
    contribuyente_id = request.data['contribuyente_id']
    password_text = request.data['password']
    contribuyente = Contribuyente.objects.get(pk=contribuyente_id)
    if contribuyente.encrypted_key == None:
        print("Generando llave")
        key = generate_key()
        contribuyente.encrypted_key = key.decode()
        contribuyente.save()
    encrypted_password = encrypt_text(password_text,contribuyente.encrypted_key.encode())
    contribuyente.password_key_firma = encrypted_password.decode()
    contribuyente.save()
    return Response("Successfully get encrypted key")
