from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password
# Create your models here.

class UserProfile(models.Model):
    user_id = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_auth = models.CharField(max_length=100, default='False')
    created = models.DateField(auto_now_add=True)
    last_login=models.DateField(auto_now=True)

    def is_authenticated(self):
        if self.is_auth is 'False':
            return False
        else:
            return True

    class Meta:
        ordering = ('created',)

class Crawler(models.Model):
    crawler_id=models.CharField(max_length=100, unique=True)
    thumbnail_url=models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ('title', 'created', 'crawler_id',)

class Subscription(models.Model):
    user_id = models.CharField(max_length=100)
    crawler_id = models.CharField(max_length=100)
    latest_pushtime = models.DateField()
    class Meta:
        ordering=('user_id', 'crawler_name',)

class PushToken(models.Model):
    user_id = models.CharField(max_length=100)
    push_token = models.CharField(max_length=100)
    class Meta:
        ordering=('user_id',)