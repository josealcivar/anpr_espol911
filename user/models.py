from django.db import models

# Create your models here.

class User(models.Model):
    nombre              = models.CharField(max_length=50)
    apellido            = models.CharField(max_length=50)
    identificacion      = models.CharField(max_length=50)
    telefono            = models.CharField(max_length=20)
    email               = models.CharField(max_length=30)
    password            = models.CharField(max_length=30)
    estado              = models.CharField(max_length=8)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)
