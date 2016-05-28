from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class TimeManager(models.Manager):
    def minutes_per_day(self, user_id):
        return Minutes.objects.filter(user_id=user_id)[0].minutes_per_day

    def hours_per_day(self, user_id):
        return self.minutes_per_day(user_id) / 60.0

class Minutes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    minutes_per_day = models.IntegerField()
    objects = TimeManager()

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
