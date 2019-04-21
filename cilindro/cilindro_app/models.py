from django.db import models


class Empresa (models.Model):
    nombre = models.CharField(max_length=20, help_text='Nombre de la empresa')
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)

    def __str__(self):
       return self.nombre


class Empleado (models.Model):
    nombre = models.CharField(max_length=20, help_text='Nombre del empleado')
    cedula = models.CharField(max_length=10)
    telefono = models.CharField(max_length=10)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, blank=False, null=True)

    def __str__(self):
       return self.nombre


class Custodio (models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE,
                                 blank=False, null=False, help_text='Representante de empresa externa')

    def __str__(self):
        return self.empleado.__str__() + ' ' + self.empleado.empresa


class Ciudad (models.Model):
    nombre = models.CharField(max_length=15, help_text='Nombre de la ciudad')
    latitud = models.FloatField(null=True, blank=True, default=None)
    longitud = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return self.nombre


