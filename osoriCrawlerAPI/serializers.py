from django.forms import widgets
from rest_framework import serializers
from osoriCrawlerAPI.models import UserProfile, Crawler, Subscription

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'password', 'email', 'created', 'last_login')

class CrawlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crawler
        fields = ('name', 'created')

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user_id', 'crawler_id', 'crawler_name', 'latest_pushtime')