from django.db import models

# Create your models here.

class Vehiculo(models.Model):
    propietario     = models.CharField(max_length=50)
    placa           = models.CharField(max_length=50)
    fecha           = models.DateField()
    horacaptura     = models.CharField(max_length=20)
    camara          = models.CharField(max_length=30)

    def __str__(self):
        return '{} {}'.format(self.propietario, self.placa)
