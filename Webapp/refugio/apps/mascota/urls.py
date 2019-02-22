
from __future__ import unicode_literals,absolute_import
from django.conf.urls import url,include
from django.contrib import admin


from apps.mascota.views import index
urlpatterns = [
    url(r'^$', index),
]
