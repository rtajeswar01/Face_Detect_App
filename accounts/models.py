from django.db import models
from django.contrib.auth.hashers import make_password

class appAdmin(models.Model):
    adminID = models.AutoField(primary_key=True)
    adminNumber = models.CharField(max_length=5)
    adminName = models.CharField(max_length=255)
    adminPassword = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        self.adminPassword = make_password(self.adminPassword)
        super().save(*args, **kwargs)