from rest_framework.serializers import *
from .models import Recipe, Role, Privilege, Tag, Profile, User

class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('__all__')
        
class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ('__all__')
        
class PrivilegeSerializer(ModelSerializer):
    class Meta:
        model = Privilege
        fields = ('__all__')
        
class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')
        
class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('__all__')
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

