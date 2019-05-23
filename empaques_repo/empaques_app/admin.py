from django.contrib import admin
from .models import *
from django.db.models import Q

admin.site.register(Modelo)

def custom_titled_filter(title):
    '''
    Custom filter admin tittle
    :param title: Filter's tittle
    '''
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

admin.site.register(Ciudad)
admin.site.register(Marca)

class BodegaAdmin (admin.ModelAdmin):
    model = Bodega
    list_display = [
        'nombre',
        'ciudad'
    ]
    list_filter = [
        'ciudad'
    ]

admin.site.register(Bodega, BodegaAdmin)


class EstadoDispAdmin (admin.ModelAdmin):
    model = Estado_disponibilidad
    list_display = [
        'nombre',
        'descripcion'
    ]
    list_editable = [
        'descripcion'
    ]

admin.site.register(Estado_disponibilidad, EstadoDispAdmin)


class ClaseAdmin (admin.ModelAdmin):
    model = Clase
    list_display = [
        'nombre',
        'descripcion'
    ]

admin.site.register(Clase, ClaseAdmin)


class Tipo_EmpAdmin (admin.ModelAdmin):
    model = Tipo_empaque
    list_display = [
        'nombre',
        'descripcion'
    ]

admin.site.register(Tipo_empaque, Tipo_EmpAdmin)


class EmpresaAdmin (admin.ModelAdmin):
    model = Empresa
    list_display = [
        'nombre',
        'codigo',
        'RUC',
        'direccion',
        'telefono'
    ]

admin.site.register(Empresa, EmpresaAdmin)


class RepresentanteAdmin (admin.ModelAdmin):
    model = Representante_empresa
    list_display = [
        'nombre',
        'cedula',
        'nombre_carta',
        'telefono',
        'empresa',
        'get_correos'
    ]
    list_editable = [
        'empresa'
    ]

    def get_correos(self, obj):
        print(obj)
        return '; '.join([p.__str__() for p in obj.correos.all()])
    get_correos.short_description = 'Correos'


admin.site.register(Representante_empresa, RepresentanteAdmin)


class Estado_empaqueAdmin (admin.ModelAdmin):
    model = Estado_empaque
    list_display = [
        'nombre',
        'descripcion'
    ]
    list_editable = [
        'descripcion'
    ]

admin.site.register(Estado_empaque, Estado_empaqueAdmin)


class CustodioAdmin (admin.ModelAdmin):
    model = Custodio
    list_display = [
        '__str__',
        'get_rep_nombre',
        'get_rep_empresa',
        'get_vendedor'
    ]

    def get_rep_nombre(self, obj):
        return obj.representante.nombre
    get_rep_nombre.short_description = 'Nombre'

    def get_rep_empresa(self, obj):
        return obj.representante.empresa.__str__()
    get_rep_empresa.short_description = 'Empresa'

    def get_vendedor(self, obj):
        return obj.vendedor.nombre
    get_vendedor.short_description = 'Vendedor'

admin.site.register(Custodio, CustodioAdmin)


class UbicacionAdmin (admin.ModelAdmin):
    model = Ubicacion
    list_display = [
        'get_str',
        'get_ciudad',
        'bodega',
        'get_estado_disp',
    ]

    list_filter = [
        'bodega__ciudad',
        ('bodega__nombre', custom_titled_filter('Bodega')),
        ('estado_disp', custom_titled_filter('Estado Disponibilidad')),
    ]

    def get_str(self, obj):
        return obj.__str__()
    get_str.short_description = 'Ubicacion'

    def get_ciudad(self, obj):
        return obj.bodega.ciudad
    get_ciudad.short_description = 'Ciudad'

    def get_estado_disp(self, obj):
        return obj.estado_disp
    get_estado_disp.short_description = 'Disponibilidad'

admin.site.register(Ubicacion, UbicacionAdmin)


class EmpaqueAdmin (admin.ModelAdmin):
    model = Empaque
    list_display = [
        '__str__',
        'codigo',
        'codigo_barras',
        'serie',
        'tipo_empaque',
        'marca',
        'clase',
        'modelo',
        'estado',
        'ubicacion',
        'get_costo',
        'get_precio',
        'custodio'
    ]

    list_filter = [
        ('tipo_empaque', custom_titled_filter('Tipo Empaque')),
        'marca',
        'modelo',
        'clase',
        'ubicacion',
        ('custodio__representante', (custom_titled_filter('Custodio'))),
    ]

    def get_costo(self, obj):
        if obj.costo == None:
            return 'NA'
        return '$ {}'.format(obj.costo)
    get_costo.show_description = 'Costo'

    def get_precio(self, obj):
        if obj.precio == None:
            return 'NA'
        return '$ {}'.format(obj.precio)
    get_precio.show_description = 'Precio'


admin.site.register(Empaque, EmpaqueAdmin)
admin.site.register(Correo)


class OrdenAdmin (admin.ModelAdmin):
    model = Orden
    list_display = [
        '__str__',
        'tipo',
        'descripcion',
        'fecha_creacion',
        'fecha_aprobacion',
        'ubicacion_inicial',
        'aprobado',
        'nueva_ubicacion',
        'nuevo_custodio',
        'completo'
    ]

    list_filter = [
        'tipo',
        'fecha_creacion',
        'ubicacion_inicial',
        'aprobado',
        'completo'
    ]

admin.site.register(Tipo_orden)
admin.site.register(Orden, OrdenAdmin)

class OrdenEmpaqueDetailAdmin (admin.ModelAdmin):
    model = OrdenEmpaquesDetail
    list_display = [
        '__str__',
        'orden_id',
        'empaque_id',
        'aprobado',
        'entregado'
    ]

    list_filter = [
        'orden_id',
        'empaque_id',
        'aprobado',
        'entregado'
    ]

admin.site.register(OrdenEmpaquesDetail, OrdenEmpaqueDetailAdmin)