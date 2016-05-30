import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):

    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    file = models.CharField(max_length=400)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    liked_list = models.CommaSeparatedIntegerField(max_length=200, default="")

    def was_published_recently(self):
        return self.pub_date >= timezone.now()- datetime.timedelta(days=1)

    def __str__(self):
        return self.text


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friend_list = models.CommaSeparatedIntegerField(max_length=200)
    profile_pic = models.CharField(max_length=200, null=True)

    def __str__(self):
        if not self.user.first_name or not self.user.last_name:
            return self.user.username

        return self.user.first_name + " " + self.user.last_name


class Like(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

