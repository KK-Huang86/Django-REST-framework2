from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)