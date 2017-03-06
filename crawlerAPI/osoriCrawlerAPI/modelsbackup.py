from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password
# Create your models here.

'''Models for user profile'''
class UserProfile(models.Model):
    user_id = models.EmailField(primary_key=True)
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
    
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return UserProfile(value)

    def to_python(self, value):
        if isinstance(value, UserProfile):
            return value
        if value is None:
            return value
        return UserProfile(value)

    class Meta:
        ordering = ('created',)

'''Models for Crawler'''
class Crawler(models.Model):
    crawler_id=models.CharField(max_length=100, primary_key= True)
    thumbnail_url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return Crawler(value)

    def to_python(self, value):
        if isinstance(value, Crawler):
            return value
        if value is None:
            return value
        return Crawler(value)

    class Meta:
        ordering = ('title', 'created', 'crawler_id',)

'''Models for Information of who subscript which crawlers'''
class Subscription(models.Model):
    user_id = models.CharField(max_length=100)
    crawler_id = models.CharField(max_length=100)
    latest_pushtime = models.DateField(auto_now_add=True)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return Subscription(value)

    def to_python(self, value):
        if isinstance(value, Subscription):
            return value
        if value is None:
            return value
        return Subscription(value)

    class Meta:
        ordering=('user_id', 'crawler_id',)
        unique_together = (('user_id', 'crawler_id'),)

'''Models for user and who`s device token'''
class PushToken(models.Model):
    user_id = models.CharField(max_length=100)
    push_token = models.CharField(max_length=300)
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return PushToken(value)

    def to_python(self, value):
        if isinstance(value, PushToken):
            return value
        if value is None:
            return value
        return PushToken(value)
    
    class Meta:
        ordering=('user_id',)
        unique_together = (('user_id', 'push_token'),)
