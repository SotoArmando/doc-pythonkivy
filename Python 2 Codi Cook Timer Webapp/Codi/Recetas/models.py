# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

    

class Instruccion(models.Model):
    titulo = models.CharField(max_length=30)
    descripcion = models.TextField(max_length = 120)

    def __str__(self):
        return "%s" % self.titulo
class Ingrediente(models.Model):
    titulo = models.CharField(max_length=30)
    cantidad = models.IntegerField()

    def __str__(self):
        return "%s" % self.titulo
class Receta(models.Model):
    titulo = models.CharField(max_length=30)
    pasos = models.CharField(max_length=30)
    instrucciones = models.ManyToManyField(Instruccion)
    ingredientes = models.ManyToManyField(Ingrediente)
    picture = models.ImageField(upload_to='pics')

    def __str__(self):
        return "%s" % self.titulo