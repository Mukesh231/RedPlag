from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    org_name = models.CharField(max_length=200, verbose_name=("Organisation name"))
    org_code = models.CharField(max_length=200, verbose_name=("Organisation password"))

class Organisation(models.Model):
    organame = models.CharField(max_length=200, verbose_name=("Organisation name"))
    orgacode = models.CharField(max_length=200, verbose_name=("Organisation password"))