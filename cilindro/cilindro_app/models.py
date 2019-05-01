from django.db import models
from django.core.validators import MaxLengthValidator, RegexValidator

class Clase (models.Model):  # Servicio listo (lista, creacion, edicion y eliminar)
    '''
        Clasificacion del empaque
    '''
    nombre = models.CharField(max_length=10, help_text='Clase del empaque (ej. Cilindros: C1, C2)')
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Tipo_empaque (models.Model):  # Servicio listo (listar)
    '''
        Tipo de empaque (cilindros, pallets, entre otros)
    '''
    nombre = models.CharField(max_length=10, help_text='Tipo de empaque (ej. Cilindro, pallet, etc')
    descripcion = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Estado_empaque (models.Model): # Servicio listo (listar, crear, modificar)
    '''
        Estado fisico del empaque
    '''
    nombre = models.CharField(max_length=10, help_text='Estado del empaque (bueno, danado, en reparacion...)')
    descripcion = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Marca (models.Model): # Servicio (listar, crear, modificar)
    '''
        Fabricante del empaque
    '''
    nombre = models.CharField(max_length=10, help_text='Nombre del fabricante del empaque')
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Modelo (models.Model): # Servicio (listar, crear, modificar)
    '''
        Modelo del empaque
    '''
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Ciudad (models.Model):  # sin servicio
    '''
        Ciudad de la bodega
    '''
    nombre = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Bodega (models.Model):  # Sin servicio
    '''
    Deposito de empaques
    '''
    nombre = models.CharField(max_length=10, help_text='Nombre de bodega')
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.nombre


class Estado_disponibilidad (models.Model):  # sin servicio
    '''
        Estado de disponibilidad del empaque (ej. Lleno, Vacio, en uso)
    '''
    nombre = models.CharField(max_length=10, help_text='Ej. Lleno, Vacio, En Uso')
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

    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=15, null=False, blank=False)
    RUC = models.CharField(max_length=13)
    direccion = models.CharField(max_length=20, null=True, blank=True)
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
    correos = models.ManyToManyField(Correo, null=True, blank=True)

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

    codigo = models.CharField(max_length=8, primary_key=True)
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

