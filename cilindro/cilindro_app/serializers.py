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