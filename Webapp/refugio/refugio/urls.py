
from __future__ import unicode_literals,absolute_import
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mascota/', include('apps.mascota.urls')),
    url(r'^adopcion/', include('apps.adopcion.urls'))
]
