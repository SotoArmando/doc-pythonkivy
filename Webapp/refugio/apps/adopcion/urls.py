
from __future__ import unicode_literals,absolute_import
from django.conf.urls import url
from django.contrib import admin
from apps.adopcion.views import index_adopcion


urlpatterns = [
    url(r'^$', index_adopcion),
]
