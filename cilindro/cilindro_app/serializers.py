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
