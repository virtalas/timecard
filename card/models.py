from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
import time


class TimeManager(models.Manager):
    def minutes_per_day(self, user_id):
        return Minutes.objects.filter(user_id=user_id)[0].minutes_per_day

    def hours_per_day(self, user_id):
        return self.minutes_per_day(user_id) / 60.0

class Minutes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    minutes_per_day = models.IntegerField()
    start_date = models.DateTimeField('date started')
    end_date = models.DateTimeField('date finished', null=True)
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

    def seconds_of_work(self):
        d1_ts = time.mktime(self.start_time.timetuple())
        if self.end_time is not None:
            d2_ts = time.mktime(self.end_time.timetuple())
        else:
            d2_ts = time.mktime(timezone.now().timetuple())
        return int(d2_ts - d1_ts)

    def hours_and_minutes_of_work(self):
        seconds = self.seconds_of_work()
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return str(h) + " h " + str(m) + " min"

    def validate_date_range(self):
        if self.end_time < self.start_time:
            return False
        return True
