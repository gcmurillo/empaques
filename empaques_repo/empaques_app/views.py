from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework import mixins
from rest_framework import generics
from django.shortcuts import render

from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone


@csrf_exempt
def API_index(request):
    return render(
        request,
        'api_index.html'
    )

@api_view(['PUT'])
def despachar(request, pk):

    try:
        orden = Orden.objects.get(pk=pk)
    except Orden.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        if orden.aprobado:
            serializer = OrdenDespacho(orden, data=request.data)
            if serializer.is_valid():
                OrdenEmpaquesDetail.objects.filter(orden__id=orden.id).update(despachado=True, fecha_despacho=timezone.now())
                if orden.tipo_id == 1:
                    values = OrdenEmpaquesDetail.objects.filter(orden__id=orden.id).values_list('empaque', flat=True)
                    Empaque.objects.filter(codigo__in=values).update(ubicacion=orden.nueva_ubicacion, custodio=orden.nuevo_custodio)
                from datetime import timedelta
                d = timedelta(days=orden.dias_plazo)
                orden.fecha_despacho = timezone.now()
                orden.fecha_final = orden.fecha_despacho + d
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"errors": "No aprobado"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def llenar_empaque(request, pk):

    try:
        empaque = Empaque.objects.get(pk=pk)
    except Empaque.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        if empaque.ubicacion.estado_disp.id == 2:
            ubicacion_lleno = Ubicacion.objects.get(bodega=empaque.ubicacion.bodega, estado_disp__id=1)
            empaque.ubicacion = ubicacion_lleno
            print(empaque.ubicacion)
            empaque.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"errors": "No vacio"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCilindros(APIView):

    def post(self, request, *args, **kwargs):
        modelo64 = Modelo.objects.get(nombre='AMONIACO GAS 64 KG')
        modelo66 = Modelo.objects.get(nombre='AMONIACO GAS 66 KG')
        tipo_cilindo = Tipo_empaque.objects.get(nombre='cilindro')
        bueno = Estado_empaque.objects.get(nombre='Bueno')
        errores = []
        # print(request.data)
        cilindros = request.data
        for cilindro in cilindros:
            print(cilindro)
            try:
                custodio = Custodio.objects.filter(representante__empresa__nombre__startswith=str(cilindro['custodio']).strip())[0]
                if cilindro['estado'] == 'VACIO':
                    estado = 'Vacio'
                elif cilindro['estado'] == 'LLENO':
                    estado = 'Lleno'
                else:
                    estado = 'En Uso'
                ubicacion = Ubicacion.objects.get(bodega__nombre=cilindro['bodega'], estado_disp__nombre=estado)
                clase = Clase.objects.get(nombre=cilindro['clase'][:2])
                Empaque.objects.create(
                    codigo=cilindro['codigo'],
                    codigo_barras="00000",
                    serie=cilindro['serie'],
                    ubicacion=ubicacion,
                    clase=clase,
                    estado=bueno,
                    modelo=modelo64 if clase == 'C1' or clase == 'CI' else modelo66,
                    custodio=custodio,
                    tipo_empaque=tipo_cilindo
                )
            except Exception as e:
                print(e)
                errores.append(cilindro['codigo'])
        if len(errores) == 0:
            return Response({"datos": request.data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            print(errores)
            return Response({"cilindros": errores}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        data = request.data

        user = authenticate(username=data.get('username'), password=data.get('password'))

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            bodega = BodegaSerializer(user.bodega)
            return Response({
                'token': token.key,
                'bodega': bodega.data,
                'tipo': user.tipo
            }, status=200)
        return Response(status=400)


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


class CorreoList (mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Correo.objects.all()
    serializer_class = CorreoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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


class CustodioCreate (mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Custodio.objects.all()
    serializer_class = CustodioSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustodioDetail (mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Custodio.objects.all()
    serializer_class = CustodioDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EmpaquesList (mixins.ListModelMixin,
                    generics.GenericAPIView):
    serializer_class = EmpaqueDetailSerializer

    def get_queryset(self):
        queryset = Empaque.objects.all()
        tipo_empaque = self.request.query_params.get('tipo_empaque', None)
        clase = self.request.query_params.get('clase', None)
        modelo = self.request.query_params.get('modelo', None)
        ubicacion= self.request.query_params.get('ubicacion', None)
        bodega = self.request.query_params.get('bodega', None)
        ciudad = self.request.query_params.get('ciudad', None)
        estado = self.request.query_params.get('estado', None)
        custodio = self.request.query_params.get('custodio', None)
        completo = self.request.query_params.get('completo', None)
        estado_disp = self.request.query_params.get('estado_disp', None)
        if tipo_empaque is not None:
            queryset = queryset.filter(tipo_empaque__id=tipo_empaque)
        if clase is not None:
            queryset = queryset.filter(clase__id=clase)
        if ubicacion is not None:
            queryset = queryset.filter(ubicacion__id=ubicacion)
        if bodega is not None:
            queryset = queryset.filter(ubicacion__bodega__id=bodega)
        if ciudad is not None:
            queryset = queryset.filter(ubicacion__bodega__ciudad__id=ciudad)
        if estado is not None:
            queryset = queryset.filter(estado__id=estado)
        if custodio is not None:
            queryset = queryset.filter(custodio__id=custodio)
        if completo is not None:
            queryset = queryset.filter(completo=completo)
        if modelo is not None:
            queryset = queryset.filter(modelo__id=modelo)
        if estado_disp is not None:
            queryset = queryset.filter(ubicacion__estado_disp__id=estado_disp)
        return queryset


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EmpaqueSelectable (mixins.ListModelMixin,
                         generics.GenericAPIView):

    serializer_class = EmpaqueDetailSerializer

    def get_queryset(self):
        emps = OrdenEmpaquesDetail.objects.filter(entregado=False).values_list('empaque', flat=True)
        return Empaque.objects.filter(~Q(codigo__in=emps) & Q(estado__id=1) & Q(ubicacion__estado_disp=1))

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


class TipoOrdenList (mixins.ListModelMixin,
                     generics.GenericAPIView):
    queryset = Tipo_orden.objects.all()
    serializer_class = TipoOrdenSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrdenList (mixins.ListModelMixin,
                 generics.GenericAPIView):
    serializer_class = OrdenDetailSerializer

    def get_queryset(self):
        queryset = Orden.objects.all()
        tipo = self.request.query_params.get('tipo', None)
        despachado = self.request.query_params.get('despachado', None)
        if tipo is not None:
            queryset = queryset.filter(tipo__id=tipo)
        if despachado is not None:
            queryset = queryset.filter(despachado=despachado)
        return queryset


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrdenCreate (mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = Orden.objects.all()
    serializer_class = OrdenCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrdenUpdate (mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    queryset = Orden.objects.all()
    serializer_class = OrdenDetailSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OrdenEmpaqueDetailList (mixins.ListModelMixin,
                              generics.GenericAPIView):
    serializer_class = OrdenEmpaqueDetailSerializer

    def get_queryset(self):
        queryset = OrdenEmpaquesDetail.objects.filter(despachado=False)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrdenEmpaqueDetailPorEntregar (mixins.ListModelMixin,
                                     generics.GenericAPIView):
    serializer_class = OrdenEmpaqueDetailSerializer

    def get_queryset(self):
        return OrdenEmpaquesDetail.objects.filter(despachado=True, entregado=False)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrdenEmpaqueDetailCreate (mixins.CreateModelMixin,
                                generics.GenericAPIView):
    queryset = OrdenEmpaquesDetail.objects.all()
    serializer_class = OrdenEmpaqueSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrdenEmpaqueDetailUpdate(mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               generics.GenericAPIView):

    queryset = OrdenEmpaquesDetail.objects.all()
    serializer_class = OrdenEmpaqueSerializer

    def put(self, request, *args, **kwargs):
        orden = OrdenEmpaquesDetail.objects.get(Q(orden__id=request.data['orden']) &
                                        Q(empaque__codigo=request.data['empaque']))
        if orden.orden.tipo.id == 1:
            empaque = Empaque.objects.get(codigo=request.data['empaque'])
            bodega = orden.orden.ubicacion_inicial.bodega
            ubicacion = Ubicacion.objects.get(bodega=bodega, estado_disp__id=2)
            empaque.ubicacion = ubicacion
            custodio = Custodio.objects.get(representante__nombre='..Brenntag')
            empaque.custodio = custodio
            empaque.save()
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

@api_view(['GET'])
def get_ordenes_por_caducar(request):

    try:
        from datetime import timedelta
        d = timedelta(days=7)
        ordenes = Orden.objects.filter(fecha_final__lte=timezone.now() + d, completo=False)
    except Orden.DoesNotExist:
        return HttpResponse(status=400)

    if request.method == 'GET':
        serializer = OrdenDetailSerializer(ordenes, many=True)
        return Response(serializer.data)
