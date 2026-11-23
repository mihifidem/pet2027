from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()   
    ciudad = models.CharField(max_length=100)
# Create your models here.
