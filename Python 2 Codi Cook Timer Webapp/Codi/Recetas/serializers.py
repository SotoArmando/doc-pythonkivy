from rest_framework import serializers
from .models import Receta, Instruccion, Ingrediente


class RecetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receta
        fields = ('__all__')

class InstruccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruccion
        fields = ('__all__')

class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ('__all__')



