from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email' #to login with email and password not by username
    REQUIRED_FIELDS = [] 


    

