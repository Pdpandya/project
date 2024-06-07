from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    mobile = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=20)
    age = models.BigIntegerField(default=13)
    pimage = models.ImageField(default=" ",upload_to='pimage/')
    
    def __str__(self):
        return self.name

    
    
