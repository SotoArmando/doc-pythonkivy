from rest_framework import serializers
from .models import Archivo, Profile, Mensage, Conversacion, Alarma

class ArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo
        fields = ('__all__')
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('__all__')
        
class MensageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensage
        fields = ('__all__')
        
class ConversacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversacion
        fields = ('__all__')
class AlarmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarma
        fields = ('__all__')

        