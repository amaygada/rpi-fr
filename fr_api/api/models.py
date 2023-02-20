from django.db import models

# Create your models here.

class Person(models.Model):
    Name = models.CharField(max_length=25, default="")
    Email = models.CharField(max_length=100, default="")
    Label = models.CharField(max_length=3, default=-1, blank=True, null=True)

class Attendance(models.Model):
    PersonID = models.CharField(max_length=3, default = 0)
    Timestamp = models.DateTimeField(blank=True)