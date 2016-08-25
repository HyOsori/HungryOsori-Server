from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from osoriCrawlerAPI.models import UserProfile, Crawler, Subscription
from osoriCrawlerAPI.serializers import UserProfileSerializer, CrawlerSerializer, SubscriptionSerializer


class UserList(APIView):
    def get(self, request, format=None):
        users=UserProfile.objects.all()
        if users.count() == 0:
            return Response('No')
        userSerializer = UserProfileSerializer(users, many=True)
        return Response(userSerializer.data)

    def post(self, request, format=None):
        userSerializer = UserProfileSerializer(data = request.data)
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
        uid = request.GET.get("id")
        upwd = request.GET.get("password")

        if uid:
            user = UserProfile.objects.filter(id=uid)
            if user.count() > 0:
                if user[0].password == upwd:
                    result = uid + 'Login!'
                else:
                    result = uid + ' fail to login'
            else:
                result = uid + ' does not exist'
        else:
            result = uid + ' does not exist'
        return Response(result)

    def put(self, request, id, format=None):
        user = self.get_object(id)
        userSerializer = UserProfileSerializer(user, data=request.data)
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
        except Crawler.DoesNotExise:
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
        crawler=Crawler.get_object(name)
        if crawler == False:
            Response("invalid Crawler")
        crawler.delete()
        return Response(name+" deleted")
