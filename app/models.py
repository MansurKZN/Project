from datetime import datetime
from django.contrib.auth.models import User

from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)


class WorkType(models.Model):
    name = models.CharField(max_length=200)


class WorkReport(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    engineer = models.ForeignKey(User, on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    period = models.IntegerField()
    text = models.CharField(null=True, blank=True, default=None, max_length=1000)
