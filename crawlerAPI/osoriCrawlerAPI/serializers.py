from rest_framework import serializers
from osoriCrawlerAPI.models import UserProfile, Crawler, Subscription, PushToken


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('email', 'name', 'password', 'is_auth', 'is_active', 'is_admin', 'created', 'last_login')

class CrawlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crawler
        fields = ('crawler_id', 'thumbnail_url', 'link_url', 'description', 'title', 'created')

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user_id', 'crawler_id', 'latest_pushtime')

class PushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        fields = ('user_id', 'push_token')
