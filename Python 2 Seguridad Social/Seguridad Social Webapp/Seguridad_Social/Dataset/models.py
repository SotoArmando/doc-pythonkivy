from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Archivo(models.Model):
    FECHA_CREACION = models.CharField(max_length=10)
    NOMBRES = models.CharField(max_length=40)
    APPELLIDOS = models.CharField(max_length=40)
    DATOS_ADICIONALES = models.CharField(max_length=40)
    DNI = models.CharField(max_length=40)
    HORA_CREACION = models.CharField(max_length=40)
    FECHA_DE_NACIMIENTO = models.CharField(max_length=10)
    NACIONALIDAD = models.CharField(max_length=40)
    
    
    def __str__(self):
        return "%s" % self.NOMBRES
class Profile(models.Model):
    USUARIO = models.CharField(max_length=10)
    PW = models.CharField(max_length=10)
    PIN = models.CharField(max_length=40)
    NOMBRES = models.CharField(max_length=10)
    APELLIDOS = models.CharField(max_length=10)
    DNI = models.CharField(max_length=40)
    PRV = models.CharField(max_length=40)
    CORREO = models.CharField(max_length=40)
    FECHA_CREACION = models.CharField(max_length=40)
    ESTADO = models.CharField(max_length=40)
    CONTACTOS = models.TextField()
    DIVISION = models.CharField(max_length=40)
    
class Mensage(models.Model):
    EMISOR = models.CharField(max_length=40)
    RECEPTOR = models.CharField(max_length=40)
    TEXTO = models.CharField(max_length=40)
    IMAGEN = models.FileField(blank=True,null=True)
    VIDEO = models.FileField(blank=True,null=True)
    AUDIO = models.FileField(blank=True,null=True)
    
class Conversacion(models.Model):
    PARTICIPANTES = models.CharField(max_length=40)
    FECHA_CREACION = models.TextField()
    ULTIMA_ACTIVIDAD = models.TextField()
    
class Alarma(models.Model):
    POSICION = models.CharField(max_length=100)
    GRAVEDAD = models.CharField(max_length=100)
    POSICIONRELATIVA = models.CharField(max_length=40)
    DIRECCION = models.CharField(max_length=100)
