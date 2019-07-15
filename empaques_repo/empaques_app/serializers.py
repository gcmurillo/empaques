from rest_framework import serializers, fields
from .models import *
from django.db.models import Q

class ClaseSerializer (serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'


class TipoEmpaqueSerializer (serializers.ModelSerializer):
    class Meta:
        model = Tipo_empaque
        fields = '__all__'


class Estado_empaqueSerializer (serializers.ModelSerializer):
    class Meta:
        model = Estado_empaque
        fields = '__all__'


class MarcaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'


class ModeloSerializer (serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__'


class CiudadSerializer (serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = '__all__'


class BodegaSerializer (serializers.ModelSerializer):
    ciudad = CiudadSerializer()

    class Meta:
        model = Bodega
        fields = '__all__'


class EstadoDispSerializer (serializers.ModelSerializer):
    class Meta:
        model = Estado_disponibilidad
        fields = '__all__'


class UbicacionSerializer (serializers.ModelSerializer):
    bodega = BodegaSerializer()
    estado_disp = EstadoDispSerializer()

    class Meta:
        model = Ubicacion
        fields = [
            'id',
            '__str__',
            'bodega',
            'estado_disp',
        ]


class EmpresaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class CorreoSerializer (serializers.ModelSerializer):
    class Meta:
        model = Correo
        fields = '__all__'


class RepresentanteSerializer (serializers.ModelSerializer):

    class Meta:
        model = Representante_empresa
        fields = ['id',
                  '__str__',
                  'cedula',
                  'nombre',
                  'nombre_carta',
                  'telefono',
                  'empresa',
                  'correos',
                  ]


class RepreSerializer (serializers.ModelSerializer):  # para detalle
    correos = CorreoSerializer(many=True)
    empresa = EmpresaSerializer()

    class Meta:
        model = Representante_empresa
        fields = [
            'id',
            'nombre',
            'nombre_carta',
            'empresa',
            'telefono',
            'correos'
        ]


class VendedorSerializer (serializers.ModelSerializer):

    class Meta:
        model = Representante_empresa
        fields = [
            'id',
            'nombre',
            'cedula'
        ]


class CustodioSerializer (serializers.ModelSerializer):

    class Meta:
        model = Custodio
        fields = [
            'id',
            '__str__',
            'representante',
            'vendedor'
        ]



class CustodioDetailSerializer (serializers.ModelSerializer):
    representante = RepreSerializer()
    vendedor = VendedorSerializer()

    class Meta:
        model = Custodio
        fields = [
            'id',
            '__str__',
            'representante',
            'vendedor'
        ]


class EmpaqueDetailSerializer (serializers.ModelSerializer):
    tipo_empaque = TipoEmpaqueSerializer()
    marca = MarcaSerializer()
    clase = ClaseSerializer()
    modelo = ModeloSerializer()
    estado = Estado_empaqueSerializer()
    ubicacion = UbicacionSerializer()
    custodio = CustodioDetailSerializer()

    class Meta:
        model = Empaque
        fields = [
            '__str__',
            'codigo',
            'codigo_barras',
            'serie',
            'tipo_empaque',
            'marca',
            'clase',
            'modelo',
            'modelo',
            'estado',
            'ubicacion',
            'custodio',
            'costo',
            'precio',
        ]


class EmpaqueSerializer (serializers.ModelSerializer):

    class Meta:
        model = Empaque
        fields = [
            '__str__',
            'codigo',
            'codigo_barras',
            'serie',
            'tipo_empaque',
            'marca',
            'clase',
            'modelo',
            'modelo',
            'estado',
            'ubicacion',
            'custodio',
            'costo',
            'precio',
        ]


class TipoOrdenSerializer (serializers.ModelSerializer):

    class Meta:
        model = Tipo_orden
        fields = '__all__'


class OrdenCreateSerializer (serializers.ModelSerializer):

    # fecha_inicio = fields.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = Orden
        fields = [
            '__str__',
            'tipo',
            'nombre',
            'descripcion',
            'ubicacion_inicial',
            'aprobado',
            'nueva_ubicacion',
            'nuevo_custodio',
            'fecha_inicio',
            'dias_plazo',
        ]

class OrdenEmpaqueSetSerializer (serializers.ModelSerializer):

    empaque = EmpaqueDetailSerializer()

    class Meta:
        model = OrdenEmpaquesDetail
        fields =[
            'entregado',
            'aprobado',
            'empaque'
        ]




class OrdenDetailSerializer (serializers.ModelSerializer):

    tipo = TipoOrdenSerializer()
    ubicacion_inicial = UbicacionSerializer()
    nueva_ubicacion = UbicacionSerializer()
    nuevo_custodio = CustodioDetailSerializer()
    empaques = serializers.SerializerMethodField()

    class Meta:
        model = Orden
        depth = 1
        fields = [
            'id',
            '__str__',
            'tipo',
            'nombre',
            'descripcion',
            'fecha_creacion',
            'fecha_aprobacion',
            'ubicacion_inicial',
            'aprobado',
            'nueva_ubicacion',
            'nuevo_custodio',
            'completo',
            'despachado',
            'fecha_inicio',
            'fecha_final',
            'dias_plazo',
            'empaques',
        ]

    def get_empaques(self, object):
        empaques = OrdenEmpaquesDetail.objects.filter(orden_id=object.id).values_list('empaque', flat=True)
        qs = Empaque.objects.filter(codigo__in=empaques)
        return EmpaqueDetailSerializer(qs, many=True).data


class OrdenDespacho (serializers.ModelSerializer):

    class Meta:
        model = Orden
        fields = [
            'tipo',
            'despachado',
            'ubicacion_inicial'
        ]


class OrdenEmpaqueSerializer (serializers.ModelSerializer):

    class Meta:
        model = OrdenEmpaquesDetail
        fields = [
            'orden',
            'empaque',
            'aprobado',
            'entregado',
            'despachado',
        ]


class OrdenEmpaqueDetailSerializer (serializers.ModelSerializer):

    orden = OrdenDetailSerializer()
    empaque = EmpaqueDetailSerializer()

    class Meta:
        model = OrdenEmpaquesDetail
        fields = [
            'id',
            '__str__',
            'orden',
            'empaque',
            'aprobado',
            'entregado',
            'despachado',
        ]