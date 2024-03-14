from django.db import models

class lecturer(models.Model):
    lecturerID = models.AutoField(primary_key=True)
    lecturerNumber = models.CharField(max_length=5)
    lecturerName = models.CharField(max_length=255)
    lecturerEmail = models.EmailField(max_length=255)
    lecturerPassword = models.CharField(max_length=255)
    
    def __str__(self):
        return self.lecturerName
    