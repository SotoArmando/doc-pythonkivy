from django.shortcuts import render
from rest_framework import viewsets
from .models import Archivo, Profile, Mensage, Conversacion, Alarma
from .Serializers import ArchivoSerializer, ProfileSerializer, MensageSerializer, ConversacionSerializer,AlarmaSerializer
# Create your views here.
class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all().order_by('NOMBRES')
    serializer_class = ArchivoSerializer
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('NOMBRES')
    serializer_class = ProfileSerializer
    
class MensageViewSet(viewsets.ModelViewSet):
    queryset = Mensage.objects.all().order_by('EMISOR')
    serializer_class = MensageSerializer
    
class ConversacionViewSet(viewsets.ModelViewSet):
    queryset = Conversacion.objects.all().order_by('PARTICIPANTES')
    serializer_class = ConversacionSerializer
    
class AlarmaViewSet(viewsets.ModelViewSet):
    queryset = Alarma.objects.all().order_by('GRAVEDAD')
    serializer_class = AlarmaSerializer
