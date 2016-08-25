from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    created = models.DateField(auto_now_add=True)
    last_login=models.DateField(auto_now=True)
    class Meta:
        ordering = ('created',)

class Crawler(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('name', 'id',)

class Subscription(models.Model):
    uid = models.CharField(max_length=100)
    crawlerName = models.CharField(max_length=100)
    class Meta:
        ordering=('uid', 'crawlerName',)