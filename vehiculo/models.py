from django.db import models

# Create your models here.

class Vehiculo(models.Model):
    propietario     = models.CharField(max_length=50)
    placa           = models.CharField(max_length=50)
    fecha           = models.DateField()
    horacaptura     = models.CharField(max_length=20)
    camara          = models.CharField(max_length=30)

    # def __str__(self):
    #     return '{} {}'.format(self.propietario)

class Caracteristica(models.Model):

    marca              = models.CharField(max_length=50)
    color              = models.CharField(max_length=50)
    anio_matricula     = models.CharField(max_length=50)
    modelo             = models.CharField(max_length=50)
    clase              = models.CharField(max_length=50)
    fecha_matricula    = models.CharField(max_length=50)
    anio_vehiculo      = models.CharField(max_length=50)
    servicio           = models.CharField(max_length=50)
    fecha_caducidad    = models.CharField(max_length=50)
    vehiculo           = models.ForeignKey(Vehiculo, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.color, self.marca, self.modelo)

class Lista_negra_vehiculos(models.Model):
    comentario      = models.CharField(max_length=50)
    fecha           = models.DateField()
    vehiculo        = models.ForeignKey(Vehiculo, null=True, blank=True, on_delete=models.CASCADE)
    estado          = models.CharField(max_length=10)
