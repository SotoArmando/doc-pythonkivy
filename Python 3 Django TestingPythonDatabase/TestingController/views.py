from django.shortcuts import render
from .models import Recipe,Role,Privilege,Tag,Profile,User
from .serializers import RecipeSerializer,RoleSerializer,PrivilegeSerializer,TagSerializer,ProfileSerializer,UserSerializer
from rest_framework.viewsets import *

# Create your views here.
class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by('id')
    serializer_class = RecipeSerializer
    
class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    
class PrivilegeViewSet(ModelViewSet):
    queryset = Privilege.objects.all().order_by('id')
    serializer_class = PrivilegeSerializer
    
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer
    
class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all().order_by('id')
    serializer_class = ProfileSerializer
    
class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    

    