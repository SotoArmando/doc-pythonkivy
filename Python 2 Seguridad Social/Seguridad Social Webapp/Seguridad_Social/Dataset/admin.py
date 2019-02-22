from django.contrib import admin
from .models import Archivo, Profile, Mensage, Conversacion, Alarma
# Register your models here.
admin.site.register(Archivo)
admin.site.register(Profile)
admin.site.register(Alarma)
admin.site.register(Mensage)
admin.site.register(Conversacion)