from rest_framework import serializers
from .models import *

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
        fields = '__all__'


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
    custodio = CustodioSerializer()

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