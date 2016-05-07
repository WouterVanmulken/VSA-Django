import datetime

from django.db import models
from django.utils import timezone


class Person(models.Model):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birth_date = models.DateTimeField('Birthdate')

    def __str__(self):
        return self.first_name + " " + self.last_name


class Post(models.Model):

    poster = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now()- datetime.timedelta(days=1)

    def __str__(self):
        return self.text


