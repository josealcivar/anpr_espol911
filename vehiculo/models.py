from django.db import models

# Create your models here.


class Vehiculo(models.Model):

    placa              = models.CharField(max_length=8)
    marca              = models.CharField(max_length=50, null=True)
    color              = models.CharField(max_length=50, null=True)
    anio_matricula     = models.CharField(max_length=50, null=True)
    modelo             = models.CharField(max_length=100, null=True)
    clase              = models.CharField(max_length=50, null=True)
    fecha_matricula    = models.CharField(max_length=50, null=True)
    anio_vehiculo      = models.CharField(max_length=50, null=True)
    servicio           = models.CharField(max_length=50, null=True)
    fecha_caducidad    = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.placa, self.marca, self.color, self.modelo, self.servicio)

class Flujo_vehicular(models.Model):

    fecha           = models.DateField()
    horacaptura     = models.TimeField()
    camara          = models.CharField(max_length=30)
    vehiculo        = models.ForeignKey(Vehiculo, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return '{} {} {}'.format(self.fecha, self.horacaptura, self.camara)


class Imagen_vehiculo(models.Model):
    nombre          = models.CharField(max_length=50)
    tipo            = models.CharField(max_length=50)
    # tamanio         models.Long()

class Lista_negra_vehiculos(models.Model):
    comentario      = models.CharField(max_length=300)
    fecha           = models.DateField()
    vehiculo        = models.ForeignKey(Vehiculo, null=True, blank=True, on_delete=models.CASCADE)
    estado          = models.CharField(max_length=10)
