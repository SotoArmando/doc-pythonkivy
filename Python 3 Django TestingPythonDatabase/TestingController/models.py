from django.db import models

class Recipe(models.Model):
    Titulo = models.CharField(max_length = 64)
    Descripcion = models.CharField(max_length = 300)
    Pasos = models.CharField(max_length = 300)
    Instrucciones = models.CharField(max_length = 300)
    IMG0 = models.CharField(max_length = 64)
    IMG1 = models.CharField(max_length = 64)
    IMG2 = models.CharField(max_length = 64)
    
    def __str__(self):
        return "%s" % self.Titulo
        
class Role(models.Model):
    Name = models.CharField(max_length = 64)
    PrivilegeId = models.CharField(max_length = 5)
    
    def __str__(self):
        return "%s" % self.Name
        
class Privilege(models.Model):
    Name = models.CharField(max_length = 64)
    CanAdministrate = models.CharField(max_length = 300)
    CanAccessUserContent = models.CharField(max_length = 300)

    def __str__(self):
        return "%s" % self.Name
        
class Tag(models.Model):
    Name = models.CharField(max_length = 64)
    Color = models.CharField(max_length = 20)

    
    def __str__(self):
        return "%s" % self.Name
        
class Profile(models.Model):
    Nombres = models.CharField(max_length = 64)
    Apellidos = models.CharField(max_length = 300)
    IMG0 = models.CharField(max_length = 300)

    def __str__(self):
        return "%s" % self.Nombres

class User(models.Model):
    UCrendential = models.CharField(max_length = 64)
    PCrendential = models.CharField(max_length = 300)
    Mail = models.CharField(max_length = 300)
    IsActive = models.CharField(max_length = 300)
    DateCreated = models.CharField(max_length = 300)
    
    def __str__(self):
        return "%s" % self.UCrendential



    
