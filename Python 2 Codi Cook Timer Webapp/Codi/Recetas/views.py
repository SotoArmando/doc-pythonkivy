# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .serializers import RecetaSerializer, InstruccionSerializer, IngredienteSerializer
from .models import Receta, Instruccion, Ingrediente
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  


class RecetaViewSet(viewsets.ModelViewSet):
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	queryset = Receta.objects.all().order_by('titulo')
	serializer_class = RecetaSerializer


class InstruccionViewSet(viewsets.ModelViewSet):
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	queryset = Instruccion.objects.all().order_by('titulo')
	serializer_class = InstruccionSerializer


class IngredienteViewSet(viewsets.ModelViewSet):
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	queryset = Ingrediente.objects.all().order_by('titulo')
	serializer_class = IngredienteSerializer

