from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from rest_framework import mixins
from rest_framework import generics

@csrf_exempt
def API_index(request):
    return render(
        request,
        'api_index.html'
    )


class ClaseList (mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ClaseDetail (mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, *args, **kwargs)


class TipoEmpaqueList (mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Tipo_empaque.objects.all()
    serializer_class = TipoEmpaqueSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TipoEmpaqueDetail (mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Tipo_empaque.objects.all()
    serializer_class = TipoEmpaqueSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, *args, **kwargs)


class EstadoEmpaqueList (mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    queryset = Estado_empaque.objects.all()
    serializer_class = Estado_empaqueSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EstadoEmpaqueDetail (mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           generics.GenericAPIView):
    queryset = Estado_empaque.objects.all()
    serializer_class = Estado_empaque

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(self, *args, **kwargs)


class MarcasList (mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MarcasDetail (mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           generics.GenericAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(self, *args, **kwargs)


class ModeloList (mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ModeloDetail (mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           generics.GenericAPIView):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(self, *args, **kwargs)


class UbicacionList (mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UbicacionDetail (mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, *args, **kwargs)


class EmpresaList (mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EmpresaDetail (mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     generics.GenericAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, requets, *args, **kwargs):
        return self.update(requets, *args, **kwargs)


class RepresentanteList (mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    queryset = Representante_empresa.objects.all()
    serializer_class = RepresentanteSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RepresentanteDetail (mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           generics.GenericAPIView):
    queryset = Representante_empresa.objects.all()
    serializer_class = RepreSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class VendedorList (mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Representante_empresa.objects.filter(empresa__codigo='001')
    serializer_class = VendedorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nombre = request.data['nombre']
        cedula = request.data['cedula']
        empresa_brenntag = Empresa.objects.get(codigo='001')
        Representante_empresa.objects.create(nombre=nombre,
                                             cedula=cedula,
                                             empresa=empresa_brenntag)
        return HttpResponse(status=201)


class CustodioList (mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Custodio.objects.all()
    serializer_class = CustodioSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustodioDetail (mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Custodio.objects.all()
    serializer_class = CustodioDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class EmpaquesList (mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = Empaque.objects.all()
    serializer_class = EmpaqueDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EmpaquesCreate (mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = Empaque.objects.all()
    serializer_class = EmpaqueSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class EmpaquesDetail (mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):
    queryset = Empaque.objects.all()
    serializer_class = EmpaqueDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)


