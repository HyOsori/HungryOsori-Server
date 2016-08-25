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
    user_id = models.CharField(max_length=100)
    crawler_id = models.CharField(max_length=100)
    crawler_name = models.CharField(max_length=100)
    latest_pushtime = models.DateField()
    class Meta:
        ordering=('user_id', 'crawler_name',)