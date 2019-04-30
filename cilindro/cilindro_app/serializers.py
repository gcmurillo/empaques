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
