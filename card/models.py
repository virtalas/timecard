from __future__ import unicode_literals
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=500)
    salt = models.CharField(max_length=500)
    minutes_per_day = models.IntegerField()
    balance_correction = models.IntegerField(default=0, null=True)

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField('date started')
    end_date = models.DateTimeField('date finished', null=True)

class Work(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_time = models.DateTimeField('date started')
    end_time = models.DateTimeField('date finished', null=True)
