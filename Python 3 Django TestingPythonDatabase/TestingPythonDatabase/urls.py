"""TestingPythonDatabase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from TestingController.views import RecipeViewSet,RoleViewSet,PrivilegeViewSet,TagViewSet,ProfileViewSet,UserViewSet

router = routers.DefaultRouter()
router.register(r'RecipesIndex',RecipeViewSet, base_name='a')
router.register(r'PrivilegeIndex',PrivilegeViewSet, base_name='b')
router.register(r'RoleCatalog',RoleViewSet, base_name='c')
router.register(r'TagIndex',TagViewSet, base_name='d')
router.register(r'UserIndex',UserViewSet, base_name='e')
router.register(r'ProfileIndex',ProfileViewSet, base_name='f')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('route/', include(router.urls))
]
