from django.contrib import admin
from .models import *

admin.site.register(Custodio)
admin.site.register(Ciudad)
admin.site.register(Empaque)
admin.site.register(Empresa)
admin.site.register(Bodega)
admin.site.register(Estado_disponibilidad)
admin.site.register(Estado_empaque)
admin.site.register(Ubicacion)
admin.site.register(Tipo_empaque)
admin.site.register(Clase)
admin.site.register(Representante_empresa)

# Register your models here.
