# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Persona(models.Model):
    nombres = models.CharField(max_length = 50)
    apellidos = models.CharField(max_length = 50)
    edad = models.IntegerField()
    telefono = models.CharField(max_length = 12)
    correo = models.EmailField()
    domicilio = models.TextField()