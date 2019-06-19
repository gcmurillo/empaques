from django.db import models
from django.core.validators import MaxLengthValidator, RegexValidator
from django.utils import timezone
from django.db.models import signals

class Clase (models.Model):  # Servicio listo (lista, creacion, edicion y eliminar)
    '''
        Clasificacion del empaque
    '''
    nombre = models.CharField(max_length=30, help_text='Clase del empaque (ej. Cilindros: C1, C2)')
    descripcion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Tipo_empaque (models.Model):  # Servicio listo (listar)
    '''
        Tipo de empaque (cilindros, pallets, entre otros)
    '''
    nombre = models.CharField(max_length=30, help_text='Tipo de empaque (ej. Cilindro, pallet, etc')
    descripcion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Estado_empaque (models.Model): # Servicio listo (listar, crear, modificar)
    '''
        Estado fisico del empaque
    '''
    nombre = models.CharField(max_length=30, help_text='Estado del empaque (bueno, danado, en reparacion...)')
    descripcion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Marca (models.Model): # Servicio (listar, crear, modificar)
    '''
        Fabricante del empaque
    '''
    nombre = models.CharField(max_length=30, help_text='Nombre del fabricante del empaque')
    descripcion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Modelo (models.Model): # Servicio (listar, crear, modificar)
    '''
        Modelo del empaque
    '''
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Ciudad (models.Model):  # sin servicio
    '''
        Ciudad de la bodega
    '''
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Bodega (models.Model):  # Sin servicio
    '''
    Deposito de empaques
    '''
    nombre = models.CharField(max_length=30, help_text='Nombre de bodega')
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.nombre


class Estado_disponibilidad (models.Model):  # sin servicio
    '''
        Estado de disponibilidad del empaque (ej. Lleno, Vacio, en uso)
    '''
    nombre = models.CharField(max_length=20, help_text='Ej. Lleno, Vacio, En Uso')
    descripcion = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Ubicacion (models.Model): # Servicio listo (listar)
    '''
        Direccion, y estado de disponibilidad del empaque
    '''
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, null=False, blank=False)
    estado_disp = models.ForeignKey(Estado_disponibilidad, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return '{} > {} > {}'.format(self.bodega.ciudad, self.bodega, self.estado_disp)


class Empresa (models.Model):

    regex_ruc = r'[0-9]{13}'

    codigo = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=30, null=False, blank=False)
    RUC = models.CharField(max_length=13, validators=[RegexValidator(regex_ruc)])
    direccion = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Correo (models.Model):

    correo = models.EmailField(null=False, blank=False)

    def __str__(self):
        return self.correo


class Representante_empresa (models.Model):

    cedula = models.CharField(max_length=10, null=False, blank=False)
    nombre = models.CharField(max_length=30)
    nombre_carta = models.CharField(max_length=45, blank=True, default='')
    telefono = models.CharField(max_length=10, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)
    correos = models.ManyToManyField(Correo)

    def __str__(self):
        if self.nombre == '..Brenntag':
            return self.nombre
        return '{} - {}'.format(self.nombre, self.empresa.__str__())



class Custodio (models.Model):
    representante = models.ForeignKey(Representante_empresa, on_delete=models.CASCADE, related_name='representante')
    vendedor = models.ForeignKey(Representante_empresa, on_delete=models.CASCADE, related_name='vendedor')

    def __str__(self):
        if self.representante.nombre == '..Brenntag':
            return '..Brenntag'
        return self.representante.__str__() + ' | ' + self.vendedor.nombre


class Empaque (models.Model):

    codigo = models.CharField(max_length=10, primary_key=True)
    codigo_barras = models.CharField(max_length=12)
    serie = models.CharField(max_length=12)
    tipo_empaque = models.ForeignKey(Tipo_empaque, on_delete=models.CASCADE, null=False, blank=False)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, null=True, blank=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.ForeignKey(Estado_empaque, on_delete=models.CASCADE, null=False, blank=False)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, null=False)
    costo = models.FloatField(help_text='En dolares', null=True, blank=True)
    precio = models.FloatField(help_text='En dolares', null=True, blank=True)
    custodio = models.ForeignKey(Custodio, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.tipo_empaque.__str__(), self.codigo)


## Operaciones Models

class Tipo_orden (models.Model):

    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Orden (models.Model):

    tipo = models.ForeignKey(Tipo_orden, on_delete=models.CASCADE, null=False, blank=False)
    nombre = models.CharField(max_length=30, null=True, blank=True)
    descripcion = models.CharField(max_length=50, null=True, blank=True)
    fecha_creacion = models.DateTimeField(editable=False)
    fecha_aprobacion = models.DateTimeField(editable=True, null=True, blank=True)
    ubicacion_inicial = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, null=False, blank=False, related_name="ubicacion_inicial")
    aprobado = models.BooleanField(default=False)
    nueva_ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, null=True, blank=True, related_name="nueva_ubicacion")
    nuevo_custodio = models.ForeignKey(Custodio, on_delete=models.CASCADE, null=True, blank=True)
    fecha_inicio = models.DateField(editable=True, null=True, blank=True)
    dias_plazo = models.IntegerField(null=True)
    fecha_final = models.DateField(editable=False, null=True, blank=True)
    completo = models.BooleanField(default=False,
                                   help_text='Verdadero, si en el caso de transferencia o transaccion los empaques fueron recibidos')

    def save(self, *args, **kwargs):
        '''
        On save, update fecha_creacion
        '''
        if not self.id:
            self.fecha_creacion = timezone.now()
            if self.fecha_inicio is not None and self.dias_plazo is not None:
                from datetime import timedelta
                d = timedelta(days=self.dias_plazo)
                self.fecha_final = self.fecha_inicio + d
        return super(Orden, self).save(*args, **kwargs)


    def __str__(self):
        return '{} - {}'.format(self.tipo.__str__(), self.nombre)


class OrdenEmpaquesDetail (models.Model):

    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, null=False, blank=False)
    empaque = models.ForeignKey(Empaque, on_delete=models.CASCADE, null=False, blank=False)
    aprobado = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)

    def __str__(self):
        return '{} | {}'.format(self.orden.__str__(), self.empaque.__str__())


def aprobar_orden(sender, instance, **kwargs):
    aprobados = OrdenEmpaquesDetail.objects.filter(orden__id=instance.orden.id).values_list('aprobado', flat=True)
    if len(aprobados) != 0 and False not in aprobados:
        orden = Orden.objects.get(id=instance.orden.id)
        orden.aprobado = True
        orden.save()
    else:
        orden = Orden.objects.get(id=instance.orden.id)
        orden.aprobado = False
        orden.save()


signals.post_save.connect(receiver=aprobar_orden, sender=OrdenEmpaquesDetail)