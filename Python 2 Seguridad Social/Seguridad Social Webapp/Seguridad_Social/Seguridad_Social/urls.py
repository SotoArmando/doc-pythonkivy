"""Seguridad_Social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from Dataset.views import ArchivoViewSet,ProfileViewSet,MensageViewSet,ConversacionViewSet, AlarmaViewSet
from django.conf import settings
from django.conf.urls.static import static


x = routers.DefaultRouter()
x.register(r'Archivo',ArchivoViewSet)
x.register(r'Profile',ProfileViewSet)
x.register(r'Mensage',MensageViewSet)
x.register(r'Conversacion',ConversacionViewSet)
x.register(r'Alarma',AlarmaViewSet)

  
urlpatterns = [
    url(r'^router/', include(x.urls)),
    url(r'^admin/', admin.site.urls),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
