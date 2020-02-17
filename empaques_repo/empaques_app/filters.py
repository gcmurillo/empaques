from django_filters import rest_framework as filters
from .models import Empaque, Orden, OrdenEmpaquesDetail

class EmpaqueFilter (filters.FilterSet):

    class Meta:
        model = Empaque
        fields = ['serie', 'tipo_empaque', 'custodio', 'ubicacion', 'estado']


class OrdenFilter (filters.FilterSet):

    min_fecha_inicio = filters.DateFilter(field_name='fecha_inicio', lookup_expr='gte')
    max_fecha_inicio = filters.DateFilter(field_name='fecha_inicio', lookup_expr='lte')
    fecha_inicio_rango = filters.DateRangeFilter(field_name='fecha_inicio')
    min_fecha_despacho = filters.DateFilter(field_name='fecha_despacho', lookup_expr='gte')
    max_fecha_despacho = filters.DateFilter(field_name='fecha_despacho', lookup_expr='lte')
    fecha_despacho_rango = filters.DateRangeFilter(field_name='fecha_despacho')
    min_fecha_retorno = filters.DateFilter(field_name='fecha_retorno', lookup_expr='gte')
    max_fecha_retorno = filters.DateFilter(field_name='fecha_retorno', lookup_expr='lte')
    fecha_retorno_rango = filters.DateRangeFilter(field_name='fecha_retorno')

    class Meta:
        model = Orden
        fields = ['tipo', 'completo', 'nuevo_custodio']


class OrdenEmpaqueFilter (filters.FilterSet):

    min_fecha_retorno = filters.DateFilter(field_name='fecha_retorno', lookup_expr='gte')
    max_fecha_retorno = filters.DateFilter(field_name='fecha_retorno', lookup_expr='lte')
    min_fecha_despacho = filters.DateFilter(field_name='fecha_despacho', lookup_expr='gte')
    max_fecha_despacho = filters.DateFilter(field_name='fecha_despacho', lookup_expr='lte')

    class Meta:
        model = OrdenEmpaquesDetail
        fields = ['aprobado', 'entregado', 'despachado', 'orden']