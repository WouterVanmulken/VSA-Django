import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# class Person(models.Model):
#
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     birth_date = models.DateTimeField('Birthdate', default=timezone.now())
#     #
#     # def __init__(self, first_name, last_name, birth_date):
#     #     self.first_name = first_name
#     #     self.last_name = last_name
#     #     self.birth_date = birth_date
#
#     def __str__(self):
#         return self.first_name + " " + self.last_name


class Post(models.Model):

    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    file = models.CharField(max_length=400)
    pub_date = models.DateTimeField('date published',default=timezone.now())

    # def __init__(self, poster, text):
    #     self.poster = poster
    #     self.text = text
    #     self.pub_date = timezone.now()

    def was_published_recently(self):
        return self.pub_date >= timezone.now()- datetime.timedelta(days=1)

    def __str__(self):
        return self.text


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

