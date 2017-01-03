from rest_framework import serializers
from osoriCrawlerAPI.models import UserProfile, Crawler, Subscription, PushToken


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user_id', 'name', 'password', 'is_auth', 'created', 'last_login')


class CrawlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crawler
        fields = ('crawler_id', 'thumbnail_url', 'description', 'title', 'created')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user_id', 'crawler_id', 'crawler_id', 'latest_pushtime')


class PushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        fields = ('user_id', 'push_token')
