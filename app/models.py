from datetime import datetime
from django.contrib.auth.models import AbstractUser

from django.db import models


class Manager(AbstractUser):
    work_time = models.IntegerField()
    work_position = models.CharField(max_length=100, default="")

class Project(models.Model):
    name = models.CharField(max_length=200)

class WorkType(models.Model):
    name = models.CharField(max_length=200)

class Engineer(models.Model):
    full_name = models.CharField(max_length=100)

class WorkReport(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    period = models.IntegerField()
    text = models.CharField(null=True, blank=True, default=None, max_length=1000)
