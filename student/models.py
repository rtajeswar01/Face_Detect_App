from django.db import models
from modules.models import Module

class Student(models.Model):
    studentID = models.AutoField(primary_key=True)
    studentName = models.CharField(max_length=255)
    studentNumber = models.CharField(max_length=10, unique=True)
    studentEmail = models.EmailField(unique=True)
    studentFace = models.ImageField(upload_to='student_faces/')  
    modules = models.ManyToManyField(Module)  

    def __str__(self):
        return self.studentName