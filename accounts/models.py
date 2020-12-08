from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    """!
    Inherits the default UserManager class from django.contrib.auth.models
    """
    pass

class CustomUser(AbstractUser):
    """!
    Inherits the default AbstractUser class from django.contrib.auth.models

    In addition, two more fields are added to the existing user model to facilitate authentication using organisation name and passcode during registration
    """
    org_name = models.CharField(max_length=200, verbose_name=("Organisation name"))
    org_code = models.CharField(max_length=200, verbose_name=("Organisation password"))

class Organisation(models.Model):
    """!
    Custom model to store registered organisation details.   
    
    """
    organame = models.CharField(max_length=200, verbose_name=("Organisation name"))
    orgacode = models.CharField(max_length=200, verbose_name=("Organisation password"))