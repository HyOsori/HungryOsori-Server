from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from osoriCrawlerAPI.models import UserProfile, Crawler, Subscription
from osoriCrawlerAPI.serializers import UserProfileSerializer, CrawlerSerializer, SubscriptionSerializer
from django.contrib.auth.hashers import make_password

class UserList(APIView):
    def get(self, request, format=None):
        users=UserProfile.objects.all()
        if users.count() == 0:
            return Response('No')
        userSerializer = UserProfileSerializer(users, many=True)
        return Response(userSerializer.data)

    def post(self, request, format=None):
        data = request.data
        data['password'] = make_password(password=data['password'], salt=None, hasher='default')
        userSerializer = UserProfileSerializer(data = data)
        if userSerializer.is_valid():
            userSerializer.save()
            return Response(userSerializer.data, status=status.HTTP_201_CREATED)

        return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_object(self, id):
        try:
            return UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return False

    def get(self, request, id, format=None):
        user = self.get_object(id)
        userSerializer=UserProfileSerializer(user)
        if user != None:
            return Response(userSerializer.data)
        return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        user = self.get_object(id)
        data = request.data
        data['password'] = make_password(password=data['password'], salt=None, hasher='default')
        userSerializer = UserProfileSerializer(user, data=data)
        if userSerializer.is_valid():
            userSerializer.save()
            return Response(userSerializer.data)
        return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        user=self.get_object(id)
        if user == False:
            return Response("invalid user")
        user.delete()
        return Response(id + " deleted")

class CrawlerList(APIView):
    def get(self, request, format=None):
        crawlers=Crawler.objects.all()
        crawlerSerializer=CrawlerSerializer(crawlers, many=True)
        return Response(crawlerSerializer.data)

    def post(self, request, format=None):
        crawlerSerializer=CrawlerSerializer(data=request.data)
        if crawlerSerializer.is_valid():
            crawlerSerializer.save()
            return Response(crawlerSerializer.data)
        return Response(crawlerSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrawlerDetail(APIView):
    def get_object(self, name):
        try:
            return Crawler.objects.get(name=name)
        except Crawler.DoesNotExist:
            return False

    def get(self, request, name, format=None):
        crawler= self.get_object(name)
        crawlerSerializer=CrawlerSerializer(crawler)
        return Response(crawlerSerializer.data)

    def put(self, request, name, format=None):
        crawler=self.get_object(name)
        crawlerSerializer=CrawlerSerializer(crawler, data=request.data)
        if crawlerSerializer.is_valid():
            crawlerSerializer.save()
            return Response(crawlerSerializer.data)
        return Response(crawlerSerializer.errors(), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        crawler=self.get_object(name)
        if crawler == False:
            Response("invalid Crawler")
        crawler.delete()
        return Response(name+" deleted")

class SubscriptionList(APIView):
    def get(self, request, format=None):
        subscription=Subscription.objects.all()
        subscriptionSerializer=SubscriptionSerializer(subscription, many=True)
        return Response(subscriptionSerializer.data)
    def post(self, request, format=None):
        subscriptionsSerializer=SubscriptionSerializer(data=request.data)
        if subscriptionsSerializer.is_valid():
            subscriptionsSerializer.save()
            return Response(subscriptionsSerializer.data)
        return Response(subscriptionsSerializer.errors(), status=status.HTTP_400_BAD_REQUEST)

class SubscriptionDetail(APIView):
    def get(self, request, format=None):

        user_id = request.GET.get('user_id')
        crawler_id = request.GET.get('crawler_id')
        if user_id != None:
            subscription = Subscription.objects.filter(user_id=user_id)
            if subscription.count() == 0:
                return Response("No Subscriptions", status=status.HTTP_400_BAD_REQUEST)
            subscriptionSerializer = SubscriptionSerializer(subscription, many=True)

        elif crawler_id != None:
            subscription = Subscription.objects.filter(crawler_id=crawler_id)
            if subscription.count() == 0:
                return Response("No Subscriptions", status=status.HTTP_400_BAD_REQUEST)
            subscriptionSerializer = SubscriptionSerializer(subscription, many=True)
        else:
            return Response("No Subscriptions" ,status=status.HTTP_400_BAD_REQUEST)
        return Response(subscriptionSerializer.data)

    def put(self, request, format=None):
        subscription=self.get_object(uid)
        subscriptionSerializer=CrawlerSerializer(subscription, data=request.data)
        if subscriptionSerializer.is_valid():
            subscriptionSerializer.save()
            return Response(subscriptionSerializer.data)
        return Response(subscriptionSerializer.errors(), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid, format=None):
        subscription=self.get_object(uid)
        if subscription == False:
            Response("invalid Subscription")
