from django.db import models
from lecturer.models import lecturer
from modules.models import Module
from student.models import Student

class Schedule(models.Model):
    scheduleID = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    lecturer = models.ForeignKey(lecturer, on_delete=models.SET_NULL, null=True)
    startDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()
    venueName = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.module} - {self.startDateTime} to {self.endDateTime}"